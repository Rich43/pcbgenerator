from pathlib import Path
from boardforge import Board, TOP_SILK, BOTTOM_SILK


BASE_DIR = Path(__file__).resolve().parent
FONT_PATH = BASE_DIR.parent / "fonts" / "RobotoMono.ttf"
OUTPUT_DIR = BASE_DIR.parent / "output"


def build_board():
    board = Board(width=70, height=55)
    board.set_layer_stack(["GTL", "GBL", TOP_SILK, BOTTOM_SILK])

    # 28-pin MCU in the center
    mcu = board.add_component("MCU", ref="U1", at=(35, 27))

    left_pins = [
        "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7",
        "VCC", "GND", "RST", "VIN", "3V3", "AREF",
    ]
    right_pins = [
        "D8", "D9", "D10", "D11", "D12", "D13",
        "A0", "A1", "A2", "A3", "A4", "A5", "VCC", "GND",
    ]
    mcu_pins = set(left_pins + right_pins)

    for i, name in enumerate(left_pins):
        dy = -13 + i * 2
        mcu.add_pin(name, dx=-5, dy=dy)
        mcu.add_pad(name, dx=-5, dy=dy, w=1.2, h=1.2)
    for i, name in enumerate(right_pins):
        dy = -13 + i * 2
        mcu.add_pin(name, dx=5, dy=dy)
        mcu.add_pad(name, dx=5, dy=dy, w=1.2, h=1.2)

    # Digital header along left edge
    header_d = board.add_component("HEADER", ref="J1", at=(5, 27))
    for i, name in enumerate(["D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13"]):
        dy = -13 + i * 2
        header_d.add_pin(name, dx=0, dy=dy)
        header_d.add_pad(name, dx=0, dy=dy, w=1.2, h=1.2)
        board.trace(mcu.pin(name), header_d.pin(name))

    # Analog header along right edge
    header_a = board.add_component("HEADER", ref="J2", at=(65, 23))
    analog_pins = ["A0", "A1", "A2", "A3", "A4", "A5"]
    for i, name in enumerate(analog_pins):
        dy = -5 + i * 2
        header_a.add_pin(name, dx=0, dy=dy)
        header_a.add_pad(name, dx=0, dy=dy, w=1.2, h=1.2)
        board.trace(mcu.pin(name), header_a.pin(name))

    # Power header
    pwr = board.add_component("POWER", ref="J3", at=(35, 50))
    power_pins = ["VIN", "VCC", "3V3", "GND"]
    for i, name in enumerate(power_pins):
        dx = -6 + i * 4
        pwr.add_pin(name, dx=dx, dy=0)
        pwr.add_pad(name, dx=dx, dy=0, w=1.2, h=1.2)
        if name in mcu_pins:
            board.trace(mcu.pin(name), pwr.pin(name))

    # Programming header (2x3)
    prog = board.add_component("PROG", ref="J4", at=(35, 10))
    prog_map = [
        ("MISO", "D12", -4),
        ("SCK", "D13", -2),
        ("RST", "RST", 0),
        ("MOSI", "D11", 2),
        ("VCC", "VCC", 4),
        ("GND", "GND", 6),
    ]
    for name, mcu_pin, dx in prog_map:
        prog.add_pin(name, dx=dx, dy=0)
        prog.add_pad(name, dx=dx, dy=0, w=1.2, h=1.2)
        board.trace(mcu.pin(mcu_pin), prog.pin(name))

    # Label components
    for comp in [mcu, header_d, header_a, pwr, prog]:
        board.add_text_ttf(comp.ref, font_path=str(FONT_PATH), at=(comp.at[0]-4, comp.at[1]-5), size=1.1, layer=TOP_SILK)

    return board


def main():
    board = build_board()
    board.save_svg_previews(str(OUTPUT_DIR))
    board.export_gerbers(str(OUTPUT_DIR / "arduino_like.zip"))


if __name__ == "__main__":
    main()
