from pathlib import Path
from PIL import Image, ImageDraw
from boardforge import PCB, Layer

BASE_DIR = Path(__file__).resolve().parent
FONT_PATH = BASE_DIR.parent / "fonts" / "RobotoMono.ttf"
GRAPHIC_PATH = BASE_DIR.parent / "graphics" / "torch.svg"
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

    for x, y in [(3, 3), (w - 3, 3), (w - 3, h - 3), (3, h - 3)]:
        board.hole((x, y), diameter=2.5)

    for dx in [-5, 0, 5]:
        board.hole((w/2 + dx, 5), diameter=1.2)

    fpga = board.add_component("FPGA", ref="U1", at=(w/2, h/2))
    for i, (dx, dy) in enumerate([(-3, -3), (-3, 3), (3, -3), (3, 3)], start=1):
        fpga.add_pin(f"P{i}", dx=dx, dy=dy)
        fpga.add_pad(f"P{i}", dx=dx, dy=dy, w=1.2, h=1.2)

    board.fill([(10, 20), (40, 20), (40, 30), (10, 30)], layer=Layer.BOTTOM_COPPER.value)

    board.annotate(5, 38, "Dazzler", size=1.5, layer=Layer.TOP_SILK)
    if GRAPHIC_PATH.exists():
        board.add_svg_graphic(str(GRAPHIC_PATH), layer=Layer.TOP_SILK.value, scale=0.5, at=(2, 2))

    img = Image.new("RGBA", (3, 3), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 2, 2], fill=(255, 0, 0, 255))
    board.logo(45, 35, img, scale=0.5, layer=Layer.TOP_SILK)

    return board


def main():
    board = build_board()
    board.save_svg_previews(str(OUTPUT_DIR))
    board.export_gerbers(OUTPUT_DIR / "dazzler_full.zip")


if __name__ == "__main__":
    main()
