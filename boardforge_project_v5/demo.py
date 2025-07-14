
from boardforge import Board

board = Board(width=40, height=20)

battery = board.add_component("CR2032", ref="BT1", at=(5, 10))
resistor = board.add_component("R", ref="R1", at=(15, 10))
led_center = board.add_component("LED", ref="D1", at=(25, 10))
led_left = board.add_component("LED", ref="D2", at=(25, 5), rotation=-45)
led_right = board.add_component("LED", ref="D3", at=(25, 15), rotation=45)

board.trace(battery.pin("VCC"), resistor.pin("1"))
board.trace(resistor.pin("2"), led_center.pin("A"))
board.trace(led_center.pin("K"), battery.pin("GND"))

board.add_via(20, 12)

board.export_gerbers("output/boardforge_output.zip")
