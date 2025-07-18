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
The repository also adapts several of
[James Bowman's CuFlow project](https://github.com/jamesbowman/cuflow)
examples. Currently `cuflow_demo.py` and `cuflow_clockpwr.py` are available,
and the `examples/cuflow_dazzler.py` script provides a simplified Dazzler
adaptation. These scripts translate the original CuFlow commands into
BoardForge's higher level PCB API, showing how similar layouts can be produced
while crediting the original CuFlow work.

## Running the tests

Install the dependencies and execute the test suite:

```bash
pip install -r requirements.txt
pytest
```

## License

This project is licensed under the [MIT License](LICENSE).
