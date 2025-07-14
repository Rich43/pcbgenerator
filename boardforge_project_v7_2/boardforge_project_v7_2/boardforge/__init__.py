
from pathlib import Path
import zipfile
import math
from collections import defaultdict

class Pin:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

class Pad:
    def __init__(self, name, x, y, w, h, layer="GTL"):
        self.name = name
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.layer = layer

class Component:
    def __init__(self, ref, type, at, rotation=0):
        self.ref = ref
        self.type = type
        self.at = at
        self.rotation = math.radians(rotation)
        self.pins = {}
        self.pads = []
        self.label_offset = (0, -2)

    def rotate_point(self, dx, dy):
        x = dx * math.cos(self.rotation) - dy * math.sin(self.rotation)
        y = dx * math.sin(self.rotation) + dy * math.cos(self.rotation)
        return x, y

    def add_pin(self, name, dx, dy):
        rx, ry = self.rotate_point(dx, dy)
        self.pins[name] = Pin(name, self.at[0] + rx, self.at[1] + ry)

    def add_pad(self, name, dx, dy, w, h, layer="GTL"):
        rx, ry = self.rotate_point(dx, dy)
        self.pads.append(Pad(name, self.at[0] + rx, self.at[1] + ry, w, h, layer))

    def pin(self, name):
        return self.pins[name]

class Via:
    def __init__(self, x, y, from_layer, to_layer):
        self.x = x
        self.y = y
        self.from_layer = from_layer
        self.to_layer = to_layer

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.components = []
        self.traces_by_layer = defaultdict(list)
        self.vias = []
        self.layer_stack = []

    def set_layer_stack(self, layers):
        self.layer_stack = layers

    def add_component(self, type, ref, at, rotation=0):
        comp = Component(ref, type, at, rotation)
        self.components.append(comp)
        return comp

    def trace(self, pin1, pin2, layer="GTL"):
        self.traces_by_layer[layer].append((pin1, pin2))

    def add_via(self, x, y, from_layer="GTL", to_layer="GBL"):
        self.vias.append(Via(x, y, from_layer, to_layer))

    def export_gerbers(self, output_zip_path):
        output_path = Path(output_zip_path).with_suffix('')
        output_path.mkdir(parents=True, exist_ok=True)

        all_layers = set(self.traces_by_layer.keys())
        for comp in self.components:
            for pad in comp.pads:
                all_layers.add(pad.layer)

        for layer in all_layers:
            lines = [
                "%FSLAX25Y25*%",
                "%MOIN*%",
                "%ADD10C,0.0100*%",
                "%ADD11R,0.0500X0.0500*%",
                "D10*",
            ]
            for pin1, pin2 in self.traces_by_layer.get(layer, []):
                lines.append(f"X{int(pin1.x*1000):07d}Y{int(pin1.y*1000):07d}D02*")
                lines.append(f"X{int(pin2.x*1000):07d}Y{int(pin2.y*1000):07d}D01*")
            lines.append("D11*")
            for comp in self.components:
                for pad in comp.pads:
                    if pad.layer == layer:
                        lines.append(f"X{int(pad.x*1000):07d}Y{int(pad.y*1000):07d}D03*")
            lines.append("M02*")
            with open(output_path / f"{layer}.gbr", "w") as f:
                f.write('\n'.join(lines))

        with open(output_path / "boardforge.txt", "w") as f:
            f.write("M48\nINCH,TZ\nT01C0.016\n%\nT01\n")
            for via in self.vias:
                f.write(f"X{int(via.x*1000):05d}Y{int(via.y*1000):05d}\n")
            f.write("M30")

        # Correct board outline for OSH Park (.GKO)
        outline_lines = [
            "%FSLAX25Y25*%",
            "%MOIN*%",
            "%ADD10C,0.0100*%",
            "D10*",
            f"X{int(0):07d}Y{int(0):07d}D02*",
            f"X{int(self.width*1000):07d}Y{int(0):07d}D01*",
            f"X{int(self.width*1000):07d}Y{int(self.height*1000):07d}D01*",
            f"X{int(0):07d}Y{int(self.height*1000):07d}D01*",
            f"X{int(0):07d}Y{int(0):07d}D01*",
            "M02*"
        ]
        with open(output_path / "boardforge.GKO", "w") as f:
            f.write('\n'.join(outline_lines))

        # SVG preview
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width*10}" height="{self.height*10}" viewBox="0 0 {self.width} {self.height}">']
        svg.append(f'<rect width="{self.width}" height="{self.height}" fill="none" stroke="black" stroke-width="0.2"/>')
        for layer, traces in self.traces_by_layer.items():
            for pin1, pin2 in traces:
                svg.append(f'<line x1="{pin1.x}" y1="{pin1.y}" x2="{pin2.x}" y2="{pin2.y}" stroke="green" stroke-width="0.2"/>')
        for via in self.vias:
            svg.append(f'<circle cx="{via.x}" cy="{via.y}" r="0.2" fill="blue"/>')
        for comp in self.components:
            x, y = comp.at
            svg.append(f'<g transform="rotate({math.degrees(comp.rotation):.1f},{x},{y})">')
            svg.append(f'<rect x="{x-1}" y="{y-1}" width="2" height="2" fill="none" stroke="gray"/>')
            svg.append(f'<text x="{x}" y="{y - 1.5}" font-size="1" fill="black">{comp.ref}</text>')
            for pad in comp.pads:
                svg.append(f'<rect x="{pad.x - pad.w/2}" y="{pad.y - pad.h/2}" width="{pad.w}" height="{pad.h}" fill="red"/>')
            for pin in comp.pins.values():
                svg.append(f'<circle cx="{pin.x}" cy="{pin.y}" r="0.1" fill="orange"/>')
            svg.append('</g>')
        svg.append("</svg>")
        with open(output_path / "preview.svg", "w") as f:
            f.write('\n'.join(svg))

        with zipfile.ZipFile(output_zip_path, 'w') as zipf:
            for file in output_path.iterdir():
                zipf.write(file, arcname=file.name)
