# PCB Generator Repository

This repository contains the **BoardForge** project, a Python based PCB generator.

## Directory overview

```
.
├── boardforge/                        # Python package with PCB classes
├── fonts/                             # Font files used for text rendering
├── graphics/                          # Example SVG assets
├── examples/                          # Additional usage demos
├── output/                            # Generated Gerber previews
├── demo.py                            # Demo script
├── boardforge.log                     # Example log output
├── boardforge_project_v46_grokmod.zip # Zipped copy of v46 project
├── tests/                             # Pytest suite for BoardForge
├── requirements.txt                   # Python dependencies
└── pytest.ini                         # Pytest configuration
```

Log files such as `boardforge.log` may appear when running the demos.

Example scripts in the `examples/` folder demonstrate advanced usage such as
the `arduino_like.py` microcontroller board and the
`buck_boost_converter.py` power module with display and buttons.
Two additional scripts, `cuflow_demo.py` and `cuflow_clockpwr.py`, are
adaptations of examples from [James Bowman's CuFlow project](https://github.com/jamesbowman/cuflow).
These show how similar layouts can be produced using the BoardForge API while
giving credit to the original CuFlow work.

## Running the tests

Install the dependencies and execute the test suite:

```bash
pip install -r requirements.txt
pytest
```
