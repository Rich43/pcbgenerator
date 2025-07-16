# PCB Generator Repository

This repository contains several versions of the **BoardForge** project, a Python based PCB generator.  The latest version is `boardforge_project_v46`, while earlier revisions are kept for reference.

## Directory overview

```
.
├── boardforge_project_v46/            # Current BoardForge implementation
│   ├── boardforge/                    # Python package with PCB classes
│   ├── fonts/                         # Font files used for text rendering
│   ├── graphics/                      # Example SVG assets
│   └── output/                        # Generated Gerber previews
├── boardforge_project_v46_grokmod.zip # Zipped copy of v46 project
├── boardforge_project_v5/             # Previous revision (v5)
├── boardforge_project_v7_2/           # Previous revision (v7.2)
├── boardforge_project_v7_15/          # Previous revision (v7.15)
├── boardforge_project_v7_16/          # Previous revision (v7.16)
├── boardforge_project_v7_17/          # Previous revision (v7.17)
├── tests/                             # Pytest suite for BoardForge
├── requirements.txt                   # Python dependencies
└── pytest.ini                         # Pytest configuration
```

Log files such as `boardforge.log` may appear when running the demos.

## Running the tests

Install the dependencies and execute the test suite:

```bash
pip install -r requirements.txt
pytest
```
