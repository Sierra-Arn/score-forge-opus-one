# II. Detailed Project Structure

> *This document describes the logical organization of the project codebase as a Pixi workspace for the PDF release pipeline.*

## Repository Layout

```
score-forge-opus-one/
├── composizioni/       # Musical sources for `Composizioni, Op. 1`.
│   │
│   ├── paratext/                           # Shared Typst title and copyright pages.
│   │
│   ├── Op-1_No-1_Believe/                  # No. 1: Believe (Piano).
│   ├── Op-1_No-2_Silence/                  # No. 2: Silence (Piano).
│   ├── Op-1_No-3_Abyss/                    # No. 3: Abyss (Piano, Harp, and Soprano).
│   ├── Op-1_No-4_Through_Pain/             # No. 4: Through Pain (Piano).
│   ├── Op-1_No-5_To-the-Beloved/           # No. 5: To the Beloved (Piano, Soprano, and Contralto).
│   ├── Op-1_No-6_Dreaming/                 # No. 6: Dreaming (Harp).
│   └── Op-1_No-7_Solitude-and-Loneliness/  # No. 7: Solitude and Loneliness (Piano).
│
├── recipes/            # Local conda packages built via `pixi-build` and
│   │                   # declared as workspace dependencies.
│   │
│   ├── scripts/        # PDF pipeline CLIs (pixi-build-python recipe).
│   └── musescore/      # MuseScore 3.7.0 (rattler-build recipe).
│
├── metadata.toml       # Shared release metadata (used by workspace CLIs).
│
├── pixi.toml           # Workspace manifest: channels, dependencies, and tasks.
│
├── pixi.lock           # Fully resolved and reproducible dependency lockfile.
│
├── LICENSE-CC-BY-4.0   # Full text of the Creative Commons Attribution 4.0
│                       # International License.
│
├── LICENSE-APACHE-2.0  # Full text of the Apache License, Version 2.0.
│
└── NOTICE              # Preferred attribution when reusing Apache-2.0 licensed
                        # portions of this project.
```

Source files are documented with detailed docstrings and/or inline comments to explain the code.

## Workspace Overview

### 1. `composizioni/paratext/`

Shared Typst library that produces the title and copyright pages prepended to every score. 

```
paratext/
├── lib.typ                 # Entry function: loads `metadata.toml`, sets page and document
│                           # properties, composes title and copyright pages.
│
├── 01-title-page.typ       # Title page layout (collection, number, title, instruments,
│                           # author, publication date).
│
└── 02-copyright-page.typ   # Copyright and license page (© line, CC BY 4.0 notice,
                            # rights-holder contact).
```

### 2. `composizioni/Op-1_No-*/`

One directory per piece under `composizioni/Op-1_No-*`. Every piece directory follows the same file layout, so only one example is shown below.

```
Op-1_No-1_Believe/
├── score.mscz          # MuseScore source score.
│
├── paratext.typ        # Per-piece Typst entry; imports `../paratext/lib.typ` and
│                       # supplies number, title, and instruments.
│
├── score.pdf           # MuseScore PDF export.
│
├── paratext.pdf        # Typst paratext output.
│
├── merged.pdf          # paratext.pdf + score.pdf concatenation.
│
└── release.pdf         # merged.pdf with release XMP metadata.
```

> **Note:**  
> `score.pdf`, `paratext.pdf`, `merged.pdf`, and `release.pdf` are generated artifacts and are gitignored. After a fresh clone only `score.mscz` and `paratext.typ` are present until the PDF release pipeline is run.

### 3. `recipes/scripts/`

Conda package recipe for the PDF pipeline CLIs. Exposes three CLI entry points consumed by the Pixi tasks in `pixi.toml`.

```
scripts/
├── pyproject.toml                      # Hatchling project definition and console script
│                                       # entry points.
│
├── pixi.toml                           # pixi-build-python recipe: host and run dependencies.
│
└── src/scripts/
    ├── paths.py                        # Project root resolution (PIXI_PROJECT_ROOT or
    │                                   # ancestor walk), piece path resolution, and
    │                                   # `metadata.toml` loading.
    │
    ├── typst_compile.py                # typst-compile CLI: compiles
    │                                   # `composizioni/<piece-dir>/paratext.typ` to
    │                                   # `paratext.pdf`.
    │
    ├── pdf_merge.py                    # pdf-merge CLI: concatenates `paratext.pdf` and
    │                                   # `score.pdf` into `merged.pdf`.
    │
    └── write_pdf_metadata.py           # write-pdf-metadata CLI: copies `merged.pdf` to
                                        # `release.pdf` with fresh XMP metadata.
```

All three CLIs accept a bare piece directory name (for example `Op-1_No-1_Believe`) and resolve paths relative to the workspace root. They expect the fixed file names from the piece layout above — `paratext.typ`, `score.pdf`, `paratext.pdf`, `merged.pdf`, and `release.pdf` — and will fail if those names are missing or renamed. They share `paths.py` for consistent project-root discovery and `metadata.toml` access.

### 4. `recipes/musescore/`

Conda packaging recipe for MuseScore 3.7.0. Provides the `mscore` binary (with `musescore` and `musescore3` symlinks) for exporting `score.mscz` to `score.pdf`.

```
musescore/
├── pixi.toml           # pixi-build-rattler-build package manifest.
│
├── recipe.yaml         # rattler-build recipe: git source, host and run dependencies.
│
└── build.sh            # CMake release build script. Caps parallel jobs to nproc/4 to
                        # reduce OOM risk; installs `mscore` and symlinks `musescore` and
                        # `musescore3` into PREFIX/bin.
```
