# Score Forge for Opus One

*A Pixi workspace for building publication-ready PDF scores of «Sierra Arn — Composizioni, Op. 1» from MuseScore sources.*

## Project Structure at a Glance

```
score-forge-opus-one/
├── composizioni/       # Musical sources for `Composizioni, Op. 1`. 
│                       # Each `Op-1_No-*/` subdirectory represents one musical
│                       # piece; `paratext/` represents shared Typst library.
│
├── recipes/            # Local conda packages built via `pixi-build` and 
│                       # declared as workspace dependencies. Each subdirectory
│                       # represents one local conda package recipe.
│
├── docs/               # Technical documentation covering workspace dependencies,
│                       # and detailed project structure.
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

## Quick Start

### I. Prerequisites

- [Pixi](https://pixi.sh/latest/) package manager.
- GNU/Linux-based system on `x86_64` architecture.

> **Note:**  
> These prerequisites are not strict requirements but describe the environment used for development. The project can be set up in alternative environments with different package managers, or operating systems if needed.

### II. Setup

1. **Clone the repository**

    ```bash
    git clone git@github.com:Sierra-Arn/score-forge-opus-one.git
    cd score-forge-opus-one
    ```

2. **Install dependencies**

    ```bash
    pixi install
    ```

    > **Note:**  
    > 1. MuseScore is built from source during `pixi install` and can take a considerable amount of time.
    > 2. Many compiler warnings while building MuseScore are expected and can be ignored.

3. **Activate environment**

    ```bash
    pixi shell
    ```

### III. Build

With the environment activated, publication-ready PDF scores can be rebuilt in the following steps:

1. **Launch MuseScore**

    ```bash
    musescore
    ```

    > **Note:**  
    > Messages such as `radeonsi: driver missing`, `glx: failed to create dri3 screen`, or `failed to load driver: radeonsi` may appear on launch. These warnings are expected and can be ignored if MuseScore opens and runs without crashing.

2. **Export each score to PDF through the MuseScore GUI**

    For each piece under `composizioni/Op-1_No-*/`:

    1. Open `score.mscz`.
    2. Choose **File -> Export**.
    3. Set **Export to** to **PDF file**.
    4. Set the export options:

        | Setting | Value |
        |---|---|
        | Resolution | **360 DPI** |
        | Background | **Export with background present in score** |
        | Export each score | **Combined into a single file** |

    5. Save the output as `score.pdf` in the same piece directory.

3. **Close MuseScore**

    Close the application via the window close button in the MuseScore GUI.

4. **Compile Typst title and copyright pages for every piece into `paratext.pdf`**

    ```bash
    pixi run paratext-all
    ```

5. **Merge `paratext.pdf` and `score.pdf` into `merged.pdf` for every piece**

    ```bash
    pixi run merge-all
    ```

6. **Create `release.pdf` from `merged.pdf` with release metadata for every piece**

    ```bash
    pixi run release-all
    ```

> **Want to see what happens under the hood?**  
> The Pixi tasks that drive this pipeline are defined here:
> - [Workspace tasks](./pixi.toml)
>
> Those tasks invoke the PDF pipeline CLIs. Every file is fully documented with detailed docstrings:
> - [Pipeline CLIs](./recipes/scripts/src/scripts/)

## License

Every file in this project is licensed under the [Apache License, Version 2.0](LICENSE-APACHE-2.0), except `.mscz` files, which are licensed under the [Creative Commons Attribution 4.0 International License](LICENSE-CC-BY-4.0). All files generated from the `.mscz` files, all files produced by compiling Typst code, and all files further derived from those outputs are also licensed under the [Creative Commons Attribution 4.0 International License](LICENSE-CC-BY-4.0).
