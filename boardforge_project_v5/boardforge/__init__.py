
from pathlib import Path
import zipfile
import math

class Pin:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

class Component:
    def __init__(self, ref, type, at, rotation=0):
        self.ref = ref
        self.type = type
        self.at = at  # (x, y)
        self.rotation = math.radians(rotation)
        self.pins = {}
        self.label_offset = (0, -2)

    def rotate_point(self, dx, dy):
        x = dx * math.cos(self.rotation) - dy * math.sin(self.rotation)
        y = dx * math.sin(self.rotation) + dy * math.cos(self.rotation)
        return x, y

    def add_pin(self, name, dx, dy):
        rx, ry = self.rotate_point(dx, dy)
        self.pins[name] = Pin(name, self.at[0] + rx, self.at[1] + ry)

    def pin(self, name):
        return self.pins[name]

class Via:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.components = []
        self.traces = []
        self.vias = []

    def add_component(self, type, ref, at, rotation=0):
        comp = Component(ref, type, at, rotation)
        if type == "LED":
            comp.add_pin("A", 0, 0)
            comp.add_pin("K", 2, 0)
        elif type == "R":
            comp.add_pin("1", 0, 0)
            comp.add_pin("2", 2, 0)
        elif type == "CR2032":
            comp.add_pin("VCC", 0, 0)
            comp.add_pin("GND", 5, 0)
        self.components.append(comp)
        return comp

    def trace(self, pin1, pin2):
        self.traces.append((pin1, pin2))

    def add_via(self, x, y):
        self.vias.append(Via(x, y))

    def export_gerbers(self, output_zip_path):
        output_path = Path(output_zip_path).with_suffix('')
        output_path.mkdir(parents=True, exist_ok=True)

        def write_gerber(filename, description, include_traces=False, include_vias=False):
            content = [
                f"G04 {description}*",
                "%FSLAX25Y25*%",
                "%MOIN*%",
                "%ADD10C,0.0100*%",
                "D10*",
                f"X000000Y000000D02*",
                f"X{int(self.width*1000):07d}Y000000D01*",
                f"X{int(self.width*1000):07d}Y{int(self.height*1000):07d}D01*",
                f"X000000Y{int(self.height*1000):07d}D01*",
                f"X000000Y000000D01*"
            ]

            if include_traces:
                for pin1, pin2 in self.traces:
                    content.append(f"X{int(pin1.x*1000):07d}Y{int(pin1.y*1000):07d}D02*")
                    content.append(f"X{int(pin2.x*1000):07d}Y{int(pin2.y*1000):07d}D01*")

            if include_vias:
                for via in self.vias:
                    content.append(f"X{int(via.x*1000):07d}Y{int(via.y*1000):07d}D03*")

            content.append("M02*")
            with open(output_path / filename, 'w') as f:
                f.write('\n'.join(content))

        write_gerber("boardforge.GTL", "Top copper", include_traces=True)
        write_gerber("boardforge.GBL", "Bottom copper", include_traces=True)
        write_gerber("boardforge.GTS", "Top soldermask")
        write_gerber("boardforge.GBS", "Bottom soldermask")
        write_gerber("boardforge.GTO", "Top silkscreen")
        write_gerber("boardforge.GBO", "Bottom silkscreen")
        write_gerber("boardforge.GML", "Board outline", include_vias=True)

        with open(output_path / "boardforge.TXT", "w") as f:
            f.write("M48\nINCH,TZ\nT01C0.016\n%\nT01\nX010000Y010000\nM30")

        # SVG output
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width*10}" height="{self.height*10}" viewBox="0 0 {self.width} {self.height}">']
        svg.append(f'<rect width="{self.width}" height="{self.height}" fill="none" stroke="black" stroke-width="0.2"/>')

        for pin1, pin2 in self.traces:
            svg.append(f'<line x1="{pin1.x}" y1="{pin1.y}" x2="{pin2.x}" y2="{pin2.y}" stroke="green" stroke-width="0.3"/>')

        for via in self.vias:
            svg.append(f'<circle cx="{via.x}" cy="{via.y}" r="0.3" fill="blue"/>')

        for comp in self.components:
            x, y = comp.at
            svg.append(f'<g transform="rotate({math.degrees(comp.rotation):.1f},{x},{y})">')
            svg.append(f'<rect x="{x-1}" y="{y-1}" width="2" height="2" fill="none" stroke="gray"/>')
            label_x = x + comp.label_offset[0]
            label_y = y + comp.label_offset[1]
            svg.append(f'<text x="{label_x}" y="{label_y}" font-size="1" fill="black">{comp.ref}</text>')
            svg.append('</g>')

        svg.append("</svg>")
        with open(output_path / "preview.svg", "w") as f:
            f.write('\n'.join(svg))

        # Create zip
        with zipfile.ZipFile(output_zip_path, 'w') as zipf:
            for file in output_path.iterdir():
                zipf.write(file, arcname=file.name)
