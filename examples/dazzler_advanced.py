from pathlib import Path
from boardforge import PCB, Layer

BASE_DIR = Path(__file__).resolve().parent
FONT_PATH = BASE_DIR.parent / "fonts" / "RobotoMono.ttf"
OUTPUT_DIR = BASE_DIR.parent / "output"


def build_board():
    board = PCB(width=50, height=42)
    board.set_layer_stack([
        Layer.TOP_COPPER.value,
        Layer.BOTTOM_COPPER.value,
        Layer.TOP_SILK.value,
        Layer.BOTTOM_SILK.value,
    ])

    w, h, ch = 50, 42, 3
    board.chamfer_outline(w, h, ch)

    # Mounting holes in each corner
    for x, y in [(3, 3), (w-3, 3), (w-3, h-3), (3, h-3)]:
        board.hole((x, y), diameter=2.5)

    # Left edge pads (15)
    lpitch = (h - 6) / 14
    for i in range(15):
        y = 3 + i * lpitch
        c = board.add_component("TP", ref=f"L{i+1}", at=(1.5, y))
        c.add_pin("SIG", dx=0, dy=0)
        c.add_pad("SIG", dx=0, dy=0, w=1.0, h=1.0)

    # Right edge pads (16)
    rpitch = (h - 6) / 15
    for i in range(16):
        y = 3 + i * rpitch
        c = board.add_component("TP", ref=f"R{i+1}", at=(w-1.5, y))
        c.add_pin("SIG", dx=0, dy=0)
        c.add_pad("SIG", dx=0, dy=0, w=1.0, h=1.0)

    # Optional top edge pads (5)
    tpitch = (w - 10) / 4
    for i in range(5):
        x = 5 + i * tpitch
        c = board.add_component("TP", ref=f"T{i+1}", at=(x, h-1.5))
        c.add_pin("SIG", dx=0, dy=0)
        c.add_pad("SIG", dx=0, dy=0, w=1.0, h=1.0)

    # Optional bottom edge pads (3)
    bpitch = (w - 20) / 2
    for i in range(3):
        x = 10 + i * bpitch
        c = board.add_component("TP", ref=f"B{i+1}", at=(x, 1.5))
        c.add_pin("SIG", dx=0, dy=0)
        c.add_pad("SIG", dx=0, dy=0, w=1.0, h=1.0)

    # Copper fill on bottom layer
    board.fill([(5, 5), (w-5, 5), (w-5, h-5), (5, h-5)], layer=Layer.BOTTOM_COPPER.value)

    # Silkscreen label
    board.add_text_ttf("Dazzler Advanced", font_path=str(FONT_PATH), at=(10, h/2), size=1.5, layer=Layer.TOP_SILK.value)

    return board


def main():
    board = build_board()
    board.save_svg_previews(str(OUTPUT_DIR))
    board.export_gerbers(OUTPUT_DIR / "dazzler_advanced.zip")


if __name__ == "__main__":
    main()
