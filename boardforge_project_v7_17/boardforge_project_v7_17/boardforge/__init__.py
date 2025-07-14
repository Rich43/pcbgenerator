
TOP_COPPER = "boardforge.GTL"
BOTTOM_COPPER = "boardforge.GBL"
TOP_SILK = "boardforge.GTO"
BOTTOM_SILK = "boardforge.GBO"
EDGE_CUT = "boardforge.GKO"
TOP_MASK = "boardforge.GTS"
BOTTOM_MASK = "boardforge.GBS"


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



class Graphic:
    def __init__(self, layer, commands):
        self.layer = layer
        self.commands = commands

    def render(self):
        return self.commands

class Board:
    def __init__(self):
        self.reset()

import xml.etree.ElementTree as ET

    def add_svg_graphic(self, svg_path, layer, scale=1.0, at=(0, 0)):
        tree = ET.parse(svg_path)
        root = tree.getroot()
        cmds = []
        sx, sy = at
        for el in root.iter():
            elif el.tag.endswith('ellipse'):
                cx = float(el.attrib.get("cx", 0)) * scale + sx
                cy = float(el.attrib.get("cy", 0)) * scale + sy
                rx = float(el.attrib.get("rx", 0)) * scale
                ry = float(el.attrib.get("ry", 0)) * scale
                for i in range(13):
                    a1 = 2 * 3.14159 * i / 12
                    x = cx + rx * math.cos(a1)
                    y = cy + ry * math.sin(a1)
                    cmd = f"X{int(x*1000):07d}Y{int(y*1000):07d}"
                    cmd += "D02*" if i == 0 else "D01*"
                    cmds.append(cmd)

            elif el.tag.endswith('rect'):
                x = float(el.attrib.get("x", 0)) * scale + sx
                y = float(el.attrib.get("y", 0)) * scale + sy
                w = float(el.attrib.get("width", 0)) * scale
                h = float(el.attrib.get("height", 0)) * scale
                corners = [
                    (x, y),
                    (x + w, y),
                    (x + w, y + h),
                    (x, y + h),
                    (x, y),
                ]
                for i, (px, py) in enumerate(corners):
                    cmd = f"X{int(px*1000):07d}Y{int(py*1000):07d}" + ("D02*" if i == 0 else "D01*")
                    cmds.append(cmd)

            elif el.tag.endswith('path'):
                try:
                    from svg.path import parse_path
                    d = el.attrib.get("d", "")
                    path = parse_path(d)
                    for seg in path:
                        n = max(4, int(seg.length() / 0.2))
                        for i in range(n + 1):
                            pt = seg.point(i / n)
                            px = pt.real * scale + sx
                            py = pt.imag * scale + sy
                            code = f"X{int(px*1000):07d}Y{int(py*1000):07d}"
                            code += "D02*" if len(cmds) == 0 or cmds[-1].endswith("*D01*") else "D01*"
                            cmds.append(code)
                except ImportError:
                    print("Warning: svg.path not installed. <path> elements skipped.")

            elif el.tag.endswith('circle'):
                cx = float(el.attrib.get("cx", 0)) * scale + sx
                cy = float(el.attrib.get("cy", 0)) * scale + sy
                r = float(el.attrib.get("r", 0)) * scale
                # Approximate with octagon
                for i in range(8):
                    a1 = 2 * 3.14159 * i / 8
                    a2 = 2 * 3.14159 * (i + 1) / 8
                    x1 = cx + r * math.cos(a1)
                    y1 = cy + r * math.sin(a1)
                    x2 = cx + r * math.cos(a2)
                    y2 = cy + r * math.sin(a2)
                    cmds.append(f"X{int(x1*1000):07d}Y{int(y1*1000):07d}D02*")
                    cmds.append(f"X{int(x2*1000):07d}Y{int(y2*1000):07d}D01*")
            elif el.tag.endswith('polyline'):
                points = el.attrib.get("points", "").strip().split()
                prev = None
                for pt in points:
                    if "," in pt:
                        x, y = [float(p)*scale for p in pt.split(",")]
                        x += sx
                        y += sy
                        if prev is None:
                            cmds.append(f"X{int(x*1000):07d}Y{int(y*1000):07d}D02*")
                        else:
                            cmds.append(f"X{int(x*1000):07d}Y{int(y*1000):07d}D01*")
                        prev = (x, y)

            if el.tag.endswith('line'):
                x1 = float(el.attrib.get("x1", 0)) * scale + sx
                y1 = float(el.attrib.get("y1", 0)) * scale + sy
                x2 = float(el.attrib.get("x2", 0)) * scale + sx
                y2 = float(el.attrib.get("y2", 0)) * scale + sy
                cmds.append(f"X{int(x1*1000):07d}Y{int(y1*1000):07d}D02*")
                cmds.append(f"X{int(x2*1000):07d}Y{int(y2*1000):07d}D01*")
        self.add_graphic(layer, cmds)

    ...
    def add_graphic(self, layer, commands):
        if not hasattr(self, '_graphics'):
            self._graphics = []
        self._graphics.append(Graphic(layer, commands))
        return self

    def _render_graphics(self, output_path):
        if not hasattr(self, '_graphics'):
            return
        by_layer = {}
        for g in self._graphics:
            by_layer.setdefault(g.layer, []).extend(g.render())
        for layer, cmds in by_layer.items():
            fname = output_path / f"{layer}.gbr"
            if fname.exists():
                with open(fname, 'a') as f:
                    f.write("\n".join(cmds) + "\nM02*")
            else:
                with open(fname, 'w') as f:
                    f.write("\n".join([
                        "G04 BoardForge*",
                        "%FSLAX25Y25*%",
                        "%MOIN*%",
                        "D10*",
                        *cmds,
                        "M02*"
                    ]))

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

        self._render_silkscreen_and_mask(output_path)

        self._render_bottom_layers(output_path)

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


    def _write_layer(self, fname, lines):
        with open(fname, "w") as f:
            f.write('\n'.join([
                "G04 Generated by BoardForge*",
                "%FSLAX25Y25*%",
                "%MOIN*%",
                *lines,
                "M02*"
            ]))

    def _render_silkscreen_and_mask(self, output_path):
        # Top silkscreen (.GTO)
        silk = []
        for comp in self.components:
            x, y = comp.at
            silk.append(f"D10*")
            silk.append(f"X{int((x - 0.5)*1000):07d}Y{int((y - 1.5)*1000):07d}D02*")
            silk.append(f"X{int((x + 0.5)*1000):07d}Y{int((y - 1.5)*1000):07d}D01*")
        self._write_layer(output_path / "boardforge.GTO", silk)

        # Top soldermask (.GTS)
        mask = ["%ADD11R,0.0500X0.0500*%", "D11*"]
        for comp in self.components:
            for pad in comp.pads:
                if pad.layer == "GTL":
                    mask.append(f"X{int(pad.x*1000):07d}Y{int(pad.y*1000):07d}D03*")
        self._write_layer(output_path / "boardforge.GTS", mask)


    def _render_bottom_layers(self, output_path):
        # Bottom soldermask (GBS)
        mask = ["%ADD11R,0.0500X0.0500*%", "D11*"]
        for comp in self.components:
            for pad in comp.pads:
                if pad.layer == "GBL":
                    mask.append(f"X{int(pad.x*1000):07d}Y{int(pad.y*1000):07d}D03*")
        self._write_layer(output_path / "boardforge.GBS", mask)

        # Bottom silkscreen (GBO) — name/logo
        silk = [
            "D10*",
            
        ]
        # This will show as a line under the board name
        
        self._write_layer(output_path / "boardforge.GBO", silk)


    def obsolete_add_silkscreen_text(self, text, at, layer="GTO", size=1.0):
        x, y = at
        spacing = 1.2 * size
        char_width = 0.8 * size
        font = {
            "A": [(0,0), (0.5,1), (1,0), (0.25,0.5), (0.75,0.5)],
            "B": [(0,0), (0,1), (0.6,1), (0.7,0.8), (0.6,0.5), (0.7,0.2), (0.6,0), (0,0)],
            "O": [(0.5,0), (0,0.5), (0.5,1), (1,0.5), (0.5,0)],
            "R": [(0,0), (0,1), (0.6,1), (0.6,0.5), (0,0.5), (0.6,0)],
        }
        cmds = []
        for i, c in enumerate(text.upper()):
            if c not in font:
                continue
            points = font[c]
            ox = x + i * spacing
            for j, (px, py) in enumerate(points):
                tx = ox + px * char_width
                ty = y + py * size
                cmd = f"X{int(tx*1000):07d}Y{int(ty*1000):07d}" + ("D02*" if j==0 else "D01*")
                cmds.append(cmd)
        self.add_graphic(layer, cmds)

    def add_silkscreen_text(self, text, at, layer="GTO", size=1.0, rotation=0):
        from math import cos, sin, radians
        x, y = at
        rot = radians(rotation)
        font_file = Path(__file__).parent / "vector_font.json"
        if not font_file.exists():
            print("Missing font file")
            return
        font = json.loads(font_file.read_text())
        cmds = []
        offset = 0
        for c in text.upper():
            char = font.get(c)
            if not char:
                offset += 1.2 * size
                continue
            for stroke in char:
                for i, (px, py) in enumerate(stroke):
                    tx = x + offset + px * size
                    ty = y + py * size
                    rx = x + (tx - x) * cos(rot) - (ty - y) * sin(rot)
                    ry = y + (tx - x) * sin(rot) + (ty - y) * cos(rot)
                    cmds.append(f"X{int(rx*1000):07d}Y{int(ry*1000):07d}" + ("D02*" if i == 0 else "D01*"))
            offset += 1.2 * size
        self.add_graphic(layer, cmds)

    def add_text_ttf(self, text, at, size=1.0, rotation=0, layer="GTO"):
        from fontTools.ttLib import TTFont
        from fontTools.pens.basePen import BasePen
        from fontTools.pens.recordingPen import RecordingPen
        from fontTools.pens.transformPen import TransformPen
        import math

        class FlattenPen(BasePen):
            def __init__(self, glyphSet, scale, commands, start):
                super().__init__(glyphSet)
                self.scale = scale
                self.commands = commands
                self.start = start
                self.current = None

            def _moveTo(self, p):
                self.current = p
                x, y = p[0] * self.scale + self.start[0], p[1] * self.scale + self.start[1]
                self.commands.append(f"X{int(x):07d}Y{int(y):07d}D02*")

            def _lineTo(self, p):
                self.current = p
                x, y = p[0] * self.scale + self.start[0], p[1] * self.scale + self.start[1]
                self.commands.append(f"X{int(x):07d}Y{int(y):07d}D01*")

            def _curveToOne(self, p1, p2, p3):
                # Approximate Bézier with 10 line segments
                steps = 10
                pts = [self.current, p1, p2, p3]
                for i in range(steps + 1):
                    t = i / steps
                    x = (1 - t)**3 * pts[0][0] + 3 * (1 - t)**2 * t * pts[1][0] + 3 * (1 - t) * t**2 * pts[2][0] + t**3 * pts[3][0]
                    y = (1 - t)**3 * pts[0][1] + 3 * (1 - t)**2 * t * pts[1][1] + 3 * (1 - t) * t**2 * pts[2][1] + t**3 * pts[3][1]
                    x = x * self.scale + self.start[0]
                    y = y * self.scale + self.start[1]
                    code = f"X{int(x):07d}Y{int(y):07d}"
                    code += "D01*" if i > 0 else "D02*"
                    self.commands.append(code)

        font_path = Path(__file__).parent / "RobotoMono.ttf"
        font = TTFont(font_path)
        glyphSet = font.getGlyphSet()
        cmap = font["cmap"].getBestCmap()

        x_offset = at[0] * 1000
        y_offset = at[1] * 1000
        scale = size * 0.05
        rot_rad = math.radians(rotation)
        cmds = []

        for c in text:
            gid = cmap.get(ord(c))
            if not gid:
                x_offset += 600 * scale
                continue
            glyph = glyphSet[gid]
            pen = FlattenPen(glyphSet, scale, cmds, (x_offset, y_offset))
            glyph.draw(pen)
            x_offset += glyph.width * scale

        self.add_graphic(layer, cmds)