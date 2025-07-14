
from boardforge import Board
import os

board = Board(width=60, height=50)
board.set_layer_stack(["GTL", "GBL"])

# Add a simple CR2032 + LED layout (minimal)
bt = board.add_component("CR2032", ref="BT1", at=(30, 5))
bt.add_pin("VCC", dx=0, dy=0)
bt.add_pin("GND", dx=10, dy=0)
bt.add_pad("VCC", dx=0, dy=0, w=1.2, h=1.2)
bt.add_pad("GND", dx=10, dy=0, w=1.2, h=1.2)

led = board.add_component("LED", ref="D1", at=(30, 40))
led.add_pin("A", dx=0, dy=0)
led.add_pin("K", dx=2, dy=0)
led.add_pad("A", dx=0, dy=0, w=1.2, h=1.2)
led.add_pad("K", dx=2, dy=0, w=1.2, h=1.2)

board.trace(bt.pin("VCC"), led.pin("A"))
board.trace(led.pin("K"), bt.pin("GND"), layer="GBL")

# Load an SVG graphic
svg_path = os.path.join(os.path.dirname(__file__), "graphics", "torch.svg")
if os.path.exists(svg_path):
    board.add_svg_graphic(svg_path, layer=BOTTOM_SILK, scale=1.0, at=(10, 10))

board.export_gerbers("output/boardforge_output.zip")

board.add_text_ttf("Torch-O-Matic 3000", at=(5,50), size=1.5, layer=TOP_SILK)
