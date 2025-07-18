import math
from .Pin import Pin

class Pad:
    def __init__(self, name, comp, dx, dy, w, h, rotation=0):
        r = math.radians(rotation)
        self.name = name
        self.x = comp.at[0] + (dx * math.cos(r) - dy * math.sin(r))
        self.y = comp.at[1] + (dx * math.sin(r) + dy * math.cos(r))
        self.w = w
        self.h = h
        self.component = comp

class Component:
    def __init__(self, ref, type, at, rotation=0):
        self.ref = ref
        self.type = type
        self.at = at
        self.rotation = rotation
        self.pads = []
        self.pins = {}

    def add_pad(self, name, dx, dy, w, h):
        pad = Pad(name, self, dx, dy, w, h, self.rotation)
        self.pads.append(pad)
        return pad

    def add_pin(self, name, dx, dy):
        pin = Pin(name, self.at, dx, dy, self.rotation)
        self.pins[name] = pin
        return pin

    def pin(self, name):
        return self.pins.get(name)
