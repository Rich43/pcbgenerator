from pathlib import Path
from boardforge import PCB, Layer

# Adapted from jamesbowman's CuFlow dazzler.py
# Original source: https://github.com/jamesbowman/cuflow
# Simplified for the BoardForge API.

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.parent / "output"


def build_board():
    board = PCB(width=50, height=42)
    board.set_layer_stack([
        Layer.TOP_COPPER.value,
        Layer.BOTTOM_COPPER.value,
        Layer.TOP_SILK.value,
        Layer.BOTTOM_SILK.value,
    ])

    pitch = 2.0
    top = []
    bottom = []

    for i in range(10):
        x = 5 + i * pitch
        c = board.add_component("TP", ref=f"T{i+1}", at=(x, 40))
        c.add_pin("SIG", dx=0, dy=0)
        c.add_pad("SIG", dx=0, dy=0, w=1.2, h=1.2)
        top.append(c)

    for i in range(10):
        x = 5 + i * pitch
        c = board.add_component("TP", ref=f"B{i+1}", at=(x, 2))
        c.add_pin("SIG", dx=0, dy=0)
        c.add_pad("SIG", dx=0, dy=0, w=1.2, h=1.2)
        bottom.append(c)

    for t, b in zip(top, bottom):
        board.route_trace(f"{t.ref}:SIG", f"{b.ref}:SIG", layer=Layer.TOP_COPPER.value)

    board.outline([(0, 0), (50, 0), (50, 42), (0, 42), (0, 0)])

    return board


def main():
    board = build_board()
    board.save_svg_previews(str(OUTPUT_DIR))
    board.export_gerbers(OUTPUT_DIR / "cuflow_dazzler.zip")


if __name__ == "__main__":
    main()
