import sys
from pathlib import Path
import zipfile
import pytest

# Add the boardforge project v46 directory to sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "boardforge_project_v46"))

from boardforge import Pin, Component, Board, TOP_SILK, BOTTOM_SILK


def test_pin_rotation():
    pin = Pin("A", (10, 20), 1, 0, rotation=90)
    assert pytest.approx(pin.x, rel=1e-6) == 10
    assert pytest.approx(pin.y, rel=1e-6) == 21


def test_pad_rotation():
    comp = Component("R1", "RES", at=(0, 0), rotation=90)
    pad = comp.add_pad("P1", 1, 0, w=1, h=1)
    assert pytest.approx(pad.x, rel=1e-6) == 0
    assert pytest.approx(pad.y, rel=1e-6) == 1


def test_export_creates_zip_and_files(tmp_path):
    board = Board(width=10, height=10)
    board.set_layer_stack(["GTL", "GBL", TOP_SILK, BOTTOM_SILK])
    comp = board.add_component("TEST", ref="C1", at=(2, 2))
    comp.add_pin("A", dx=0, dy=0)
    comp.add_pin("B", dx=1, dy=0)
    board.trace(comp.pin("A"), comp.pin("B"))

    zip_path = tmp_path / "out.zip"
    board.export_gerbers(zip_path)

    assert zip_path.exists()
    with zipfile.ZipFile(zip_path) as z:
        names = set(z.namelist())
        top_png = z.read("preview_top.png") if "preview_top.png" in names else b""

    # Validate that the PNG preview is a valid image with expected dimensions
    from io import BytesIO
    from PIL import Image
    if top_png:
        with Image.open(BytesIO(top_png)) as img:
            assert img.size == (board.width * 10, board.height * 10)

    assert "GTL.gbr" in names
    assert "GTO.gbr" in names
    assert "preview_top.svg" in names
    assert "preview_top.png" in names
    assert len(top_png) > 0


def test_sample_circuit_gerber_contains_trace(tmp_path):
    board = Board(width=5, height=5)
    board.set_layer_stack(["GTL", "GBL", TOP_SILK, BOTTOM_SILK])

    r1 = board.add_component("RES", ref="R1", at=(1, 1))
    r1.add_pin("A", dx=-0.5, dy=0)
    r1.add_pin("B", dx=0.5, dy=0)
    r1.add_pad("A", dx=-0.5, dy=0, w=1, h=1)
    r1.add_pad("B", dx=0.5, dy=0, w=1, h=1)

    r2 = board.add_component("RES", ref="R2", at=(3, 1))
    r2.add_pin("A", dx=-0.5, dy=0)
    r2.add_pin("B", dx=0.5, dy=0)
    r2.add_pad("A", dx=-0.5, dy=0, w=1, h=1)
    r2.add_pad("B", dx=0.5, dy=0, w=1, h=1)

    board.trace(r1.pin("B"), r2.pin("A"))

    zip_path = tmp_path / "circuit.zip"
    board.export_gerbers(zip_path)

    assert zip_path.exists()
    with zipfile.ZipFile(zip_path) as z:
        gtl_data = z.read("GTL.gbr").decode()

    # Expect gerber trace lines formatted as coordinate commands
    assert "D02*" in gtl_data and "D01*" in gtl_data
