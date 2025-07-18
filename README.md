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
├── tests/                             # Pytest suite for BoardForge
├── requirements.txt                   # Python dependencies
└── pytest.ini                         # Pytest configuration
```

Log files such as `boardforge.log` may appear when running the demos.

Example scripts in the `examples/` folder demonstrate advanced usage such as
the `arduino_like.py` microcontroller board and the
`buck_boost_converter.py` power module with display and buttons.
Three scripts, `cuflow_demo.py`, `cuflow_clockpwr.py`, and
`cuflow_dazzler.py`, are adaptations of examples from
[James Bowman's CuFlow project](https://github.com/jamesbowman/cuflow).
These show how similar layouts can be produced using the BoardForge API while
giving credit to the original CuFlow work.

## Running the tests

Install the dependencies and execute the test suite:

```bash
pip install -r requirements.txt
pytest
```

## License

This project is licensed under the [MIT License](LICENSE).
