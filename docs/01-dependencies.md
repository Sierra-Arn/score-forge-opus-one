# I. Dependencies Overview

> *This document describes the runtime dependencies required by Score Forge for Opus One — Pixi, build backends, and workspace packages.*

## System Dependencies

| Dependency | Repository | What it is | Role in the project |
|---|---|---|---|
| Pixi | [prefix‑dev/pixi](https://github.com/prefix-dev/pixi) | Package and environment manager | 1. Resolves and installs conda dependencies. <br>2. Manages the project's virtual environment and lockfile. <br>3. Acts as the project's task runner. |
| pixi-build-python | [prefix‑dev/pixi](https://github.com/prefix-dev/pixi) | Pixi build backend for Python packages | Builds the `scripts` conda package from `pyproject.toml`. |
| pixi-build-rattler-build | [prefix‑dev/pixi](https://github.com/prefix-dev/pixi) | Pixi build backend for rattler-build recipes | Builds the `musescore` conda package from `recipe.yaml`. |

## Pixi Dependencies

| Dependency | Source | What it is | Role in the project | Upstream / runtime repositories |
|---|---|---|---|---|
| `scripts` | [recipes/scripts/<br>pixi.toml](../recipes/scripts/pixi.toml) | Python PDF pipeline CLIs | Compiles Typst paratext, merges PDFs, and writes PDF metadata. | - [python/cpython](https://github.com/python/cpython)<br>- [pypa/hatch](https://github.com/pypa/hatch)<br>- [typst/typst](https://github.com/typst/typst)<br>- [pikepdf/pikepdf](https://github.com/pikepdf/pikepdf) |
| `musescore` | [recipes/musescore/<br>pixi.toml](../recipes/musescore/pixi.toml) | Music notation application | Exports source scores to PDF. | - [Jojo-Schmitz/MuseScore](https://github.com/Jojo-Schmitz/MuseScore) |
