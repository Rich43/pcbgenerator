import math

class Pin:
    def __init__(self, name, comp_at, dx, dy, rotation=0):
        r = math.radians(rotation)
        self.name = name
        self.x = comp_at[0] + (dx * math.cos(r) - dy * math.sin(r))
        self.y = comp_at[1] + (dx * math.sin(r) + dy * math.cos(r))