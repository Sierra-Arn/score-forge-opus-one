# Copyright (c) 2026 Ilya Snegov (aka Sierra Arn)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# recipes/scripts/src/scripts/pdf_merge.py
import argparse
import sys
from pathlib import Path
from pikepdf import Pdf
from scripts.paths import find_project_root, resolve_piece_path


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """
    Parse command line arguments for pdf-merge.

    Parameters
    ----------
    argv : list of str or None, optional
        Argument vector to parse. If None, sys.argv is used. Default is None.

    Returns
    -------
    argparse.Namespace
        Parsed arguments containing piece_dir.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Merge composizioni/<piece-dir>/paratext.pdf and score.pdf "
            "into merged.pdf."
        ),
    )
    parser.add_argument(
        "piece_dir",
        help=(
            "Directory name under composizioni/, "
            "e.g. Op-1_No-1_Believe."
        ),
    )
    return parser.parse_args(argv)


def merge_piece_pdfs(piece_dir: str) -> Path:
    """
    Concatenate paratext and score PDFs for one piece via pikepdf.

    Parameters
    ----------
    piece_dir : str
        Directory name under composizioni/.

    Returns
    -------
    Path
        Absolute path of the written merged.pdf.

    Raises
    ------
    ValueError
        If piece_dir is not a bare directory name.
    FileNotFoundError
        If the piece directory or either input PDF is missing.
    """
    project_root = find_project_root()
    piece_path = resolve_piece_path(piece_dir, project_root=project_root)
    paratext_path = piece_path / "paratext.pdf"
    score_path = piece_path / "score.pdf"
    merged_path = piece_path / "merged.pdf"

    if not paratext_path.is_file():
        raise FileNotFoundError(f"paratext.pdf not found: {paratext_path}")
    if not score_path.is_file():
        raise FileNotFoundError(f"score.pdf not found: {score_path}")

    output = Pdf.new()
    version = output.pdf_version
    for source_path in (paratext_path, score_path):
        with Pdf.open(source_path) as source:
            version = max(version, source.pdf_version)
            output.pages.extend(source.pages)

    output.remove_unreferenced_resources()
    output.save(merged_path, min_version=version)
    return merged_path


def main(argv: list[str] | None = None) -> int:
    """
    CLI entry point for pdf-merge.

    Parameters
    ----------
    argv : list of str or None, optional
        Argument vector to parse. If None, sys.argv is used. Default is None.

    Returns
    -------
    int
        Process exit code. Zero on success, one on failure.
    """
    args = _parse_args(argv)
    try:
        merge_piece_pdfs(args.piece_dir)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        print("example: pdf-merge Op-1_No-1_Believe", file=sys.stderr)
        return 1
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
