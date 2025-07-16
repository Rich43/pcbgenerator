from .Component import Component
from .GerberExporter import export_gerbers
from .Pin import Pin
from .svgtools import render_text_ttf, render_svg_element
import xml.etree.ElementTree as ET
import math
import os
import re

TOP_SILK = "GTO"
BOTTOM_SILK = "GBO"

import datetime
import pprint
def log(msg, obj=None):
    with open('boardforge.log', 'a', encoding='utf-8') as f:
        f.write(f"{datetime.datetime.now().isoformat()} {msg}\n")
        if obj is not None:
            f.write(pprint.pformat(obj) + "\n")

class Board:

    def __init__(self, name="Board", width=100, height=80):
        log('ENTER __init__', locals())
        log("Board __init__ called")
        self.name = name
        self.width = width
        self.height = height
        self.components = []
        self.layers = {"GTO": [], "GBO": []}
        self._svg_text_calls = []
        self._svg_graphics_calls = []
        log('EXIT __init__', {'self': self.__dict__})

    def set_layer_stack(self, layers):
        log('ENTER set_layer_stack', locals())
        log("set_layer_stack called")
        for layer in layers:
            if layer not in self.layers:
                self.layers[layer] = []
        log('EXIT set_layer_stack', {'self': self.__dict__})

    def add_component(self, type, ref, at, rotation=0):
        log('ENTER add_component', locals())
        log("add_component called")
        comp = Component(ref, type, at, rotation)
        self.components.append(comp)
        return comp
        log('EXIT add_component', {'self': self.__dict__})

    def trace(self, pin1, pin2, layer="GTL"):
        self.layers[layer].append(("TRACE", pin1, pin2))

    def add_svg_graphic(self, svg_path, layer, scale=1.0, at=(0, 0)):
        log('ENTER add_svg_graphic', locals())
        log("add_svg_graphic called")
        self._svg_graphics_calls.append((svg_path, layer, scale, at))
        try:
            tree = ET.parse(svg_path)
            root = tree.getroot()
            for el in root.iter():
                cmds = render_svg_element(el, scale, *at)
                self.layers[layer].extend(cmds)
        except Exception as e:
            print(f"Error adding SVG graphic {svg_path}: {e}")
        log('EXIT add_svg_graphic', {'self': self.__dict__})

    def add_text_ttf(self, text, font_path, at=(0, 0), size=1.0, layer="GTO"):
        log('ENTER add_text_ttf', locals())
        log("add_text_ttf called")
        self._svg_text_calls.append((text, at, size, layer))
        try:
            gerber = render_text_ttf(text, font_path, at, size)
            self.layers[layer].extend(gerber)
        except Exception as e:
            print(f"TTF render error: {e}")
        log('EXIT add_text_ttf', {'self': self.__dict__})

    def save_svg_previews(self, outdir="."):
        log('ENTER save_svg_previews', locals())
        log("save_svg_previews called")
        width_px = int(self.width * 10)
        height_px = int(self.height * 10)
        log('EXIT save_svg_previews', {'self': self.__dict__})

        colors = {
            "board": "#5d2292",  # OSH Park purple
            "pad": "#ffc100",    # Gold
            "ring": "#ffec80",   # Lighter gold for through-hole rings
            "trace": "#ffc100",  # Gold
            "silk": "#ffffff"    # White
        }

        for side, suffix in [("GTO", "top"), ("GBO", "bottom")]:
            svg_elements = [
                f'<rect x="0" y="0" width="{width_px}" height="{height_px}" fill="{colors["board"]}" rx="16"/>'
            ]

            # Traces (placeholder: draws a line for each trace)
            for trace in self.layers.get("GTL" if side == "GTO" else "GBL", []):
                if isinstance(trace, tuple) and trace[0] == "TRACE":
                    pin1, pin2 = trace[1], trace[2]
                    x1, y1 = int(pin1.x * 10), int(pin1.y * 10)
                    x2, y2 = int(pin2.x * 10), int(pin2.y * 10)
                    svg_elements.append(
                        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colors["trace"]}" stroke-width="4"/>'
                    )

            # Pads with rotation drawn above traces
            for comp in self.components:
                for pad in getattr(comp, "pads", []):
                    x = int(pad.x * 10)
                    y = int(pad.y * 10)
                    w = int((getattr(pad, "w", 1.2) or 1.2) * 10)
                    h = int((getattr(pad, "h", 1.2) or 1.2) * 10)
                    if abs(w - h) <= 1:
                        ring_r = int((w + 6) // 2)
                        pad_r = int(w // 2)
                        svg_elements.append(
                            f'<circle cx="{x}" cy="{y}" r="{ring_r}" fill="{colors["ring"]}" stroke="#333" stroke-width="1"/>'
                        )
                        svg_elements.append(
                            f'<circle cx="{x}" cy="{y}" r="{pad_r}" fill="{colors["pad"]}" stroke="#333" stroke-width="2"/>'
                        )
                    else:
                        svg_elements.append(
                            f'<rect x="{x-w//2}" y="{y-h//2}" width="{w}" height="{h}" fill="{colors["pad"]}" stroke="#333" stroke-width="2" transform="rotate({comp.rotation},{x},{y})"/>'
                        )

            # Silkscreen text from _svg_text_calls
            for (text, at, size, lyr) in self._svg_text_calls:
                if lyr == side:
                    x = int(at[0] * 10)
                    y = int(at[1] * 10)
                    font_size = int(15 * size)
                    svg_elements.append(
                        f'<text x="{x}" y="{y}" fill="{colors["silk"]}" font-family="monospace" font-size="{font_size}">{text}</text>'
                    )

            # SVG graphics from _svg_graphics_calls
            for (svg_path, lyr, scale, at) in self._svg_graphics_calls:
                if lyr == side and os.path.exists(svg_path):
                    try:
                        tree = ET.parse(svg_path)
                        g = ET.tostring(tree.getroot(), encoding="unicode")
                        svg_elements.append(
                            f'<g transform="translate({int(at[0]*10)},{int(at[1]*10)}) scale({scale})">{g}</g>'
                        )
                    except Exception as e:
                        print(f"Error embedding SVG {svg_path}: {e}")

            # Generate SVG content with proper indentation
            svg_content = [
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{width_px}" height="{height_px}" viewBox="0 0 {width_px} {height_px}">'
            ]
            svg_content.extend(f'  {el}' for el in svg_elements)
            svg_content.append('</svg>')

            # Write to file
            os.makedirs(outdir, exist_ok=True)
            output_path = os.path.join(outdir, f"preview_{suffix}.svg")
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write('\n'.join(svg_content))
                # Convert the SVG preview to PNG for easier visual inspection
                try:
                    from cairosvg import svg2png
                    png_path = os.path.join(outdir, f"preview_{suffix}.png")
                    svg2png(bytes('\n'.join(svg_content), 'utf-8'), write_to=png_path)
                    # Simple verification: ensure the file was written and is not empty
                    if os.path.getsize(png_path) == 0:
                        os.remove(png_path)
                        raise ValueError("Generated PNG is empty")
                except Exception as e:
                    print(f"Error converting SVG to PNG: {e}")
            except Exception as e:
                print(f"Error writing SVG preview to {output_path}: {e}")


    def export_gerbers(self, out_path):
        log('ENTER export_gerbers', locals())
        log("export_gerbers called")
        export_gerbers(self, out_path)
