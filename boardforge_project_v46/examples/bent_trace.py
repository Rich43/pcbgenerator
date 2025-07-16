from pathlib import Path
from boardforge import create_bent_trace

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR.parent / "output"


def main():
    board = create_bent_trace()
    board.save_svg_previews(str(OUTPUT_DIR))
    board.export_gerbers(str(OUTPUT_DIR / "bent_trace.zip"))


if __name__ == "__main__":
    main()
