
from boardforge import Board

board = Board(width=60, height=50)
board.set_layer_stack(["GTL", "GBL"])

# CR2032 battery at bottom center
battery = board.add_component("CR2032", ref="BT1", at=(30, 5))
battery.add_pin("VCC", dx=0, dy=0)
battery.add_pin("GND", dx=10, dy=0)
battery.add_pad("VCC", dx=0, dy=0, w=1.2, h=1.2, layer="GTL")
battery.add_pad("GND", dx=10, dy=0, w=1.2, h=1.2, layer="GTL")

# Switch inline with battery
switch = board.add_component("SW", ref="SW1", at=(30, 15))
switch.add_pin("1", dx=0, dy=0)
switch.add_pin("2", dx=5, dy=0)
switch.add_pad("1", dx=0, dy=0, w=1.2, h=1.2)
switch.add_pad("2", dx=5, dy=0, w=1.2, h=1.2)

# Resistors above switch
resistors = []
for i, x in enumerate([20, 30, 40]):
    r = board.add_component("R", ref=f"R{i+1}", at=(x, 25))
    r.add_pin("1", dx=0, dy=0)
    r.add_pin("2", dx=5, dy=0)
    r.add_pad("1", dx=0, dy=0, w=1.2, h=1.2)
    r.add_pad("2", dx=5, dy=0, w=1.2, h=1.2)
    resistors.append(r)

# LEDs at top
leds = []
for i, (x, angle) in enumerate(zip([20, 30, 40], [-45, 0, 45])):
    led = board.add_component("LED", ref=f"D{i+1}", at=(x, 40), rotation=angle)
    led.add_pin("A", dx=0, dy=0)
    led.add_pin("K", dx=2, dy=0)
    led.add_pad("A", dx=0, dy=0, w=1.2, h=1.2)
    led.add_pad("K", dx=2, dy=0, w=1.2, h=1.2)
    leds.append(led)

# Wiring
for i in range(3):
    board.trace(resistors[i].pin("2"), leds[i].pin("A"), layer="GTL")
    board.trace(switch.pin("2"), resistors[i].pin("1"), layer="GTL")
board.trace(battery.pin("VCC"), switch.pin("1"), layer="GTL")
for led in leds:
    board.trace(led.pin("K"), battery.pin("GND"), layer="GBL")

board.export_gerbers("output/boardforge_output.zip")
