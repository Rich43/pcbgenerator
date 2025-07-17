import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from boardforge import Board


def test_drc_pad_clearance_warning():
    board = Board(width=5, height=5)
    board.set_layer_stack(["GTL", "GBL"])
    c1 = board.add_component("A", ref="U1", at=(0, 0))
    c1.add_pin("P", dx=0, dy=0)
    c1.add_pad("P", dx=0, dy=0, w=1, h=1)

    c2 = board.add_component("B", ref="U2", at=(0.6, 0))
    c2.add_pin("P", dx=0, dy=0)
    c2.add_pad("P", dx=0, dy=0, w=1, h=1)

    warnings = board.design_rule_check(min_clearance=0.7)
    assert any("Pad clearance" in w for w in warnings)


def test_drc_trace_width_warning():
    board = Board(width=5, height=5)
    board.set_layer_stack(["GTL", "GBL"])
    c1 = board.add_component("A", ref="U1", at=(0, 0))
    c1.add_pin("P", dx=0, dy=0)
    c1.add_pad("P", dx=0, dy=0, w=1, h=1)

    c2 = board.add_component("B", ref="U2", at=(4, 0))
    c2.add_pin("P", dx=0, dy=0)
    c2.add_pad("P", dx=0, dy=0, w=1, h=1)

    board.trace(c1.pin("P"), c2.pin("P"), width=0.1)
    warnings = board.design_rule_check(min_trace_width=0.15)
    assert any("width" in w for w in warnings)

