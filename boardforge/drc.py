"""Design Rule Checking utilities."""

import math
from typing import List


def check_board(board, min_trace_width: float = 0.15, min_clearance: float = 0.15) -> List[str]:
    """Return a list of DRC warnings for a board.

    Parameters
    ----------
    board : Board
        Board object to check.
    min_trace_width : float, optional
        Minimum allowed trace width in the board's units (defaults to 0.15).
    min_clearance : float, optional
        Minimum allowed clearance between pad edges (defaults to 0.15).
    """

    warnings = []

    # Trace width checks
    for layer_name, items in board.layers.items():
        for item in items:
            if not isinstance(item, tuple):
                continue
            if item[0] == "TRACE":
                width = item[3] if len(item) >= 4 else 1.0
                if width < min_trace_width:
                    warnings.append(
                        f"Trace on {layer_name} width {width}mm below minimum {min_trace_width}mm"
                    )
            elif item[0] == "TRACE_PATH":
                width = item[2] if len(item) >= 3 else 1.0
                if width < min_trace_width:
                    warnings.append(
                        f"Trace path on {layer_name} width {width}mm below minimum {min_trace_width}mm"
                    )

    # Pad clearance checks
    pads = []
    for comp in board.components:
        for pad in comp.pads:
            pad.component = comp
            pads.append(pad)

    for i in range(len(pads)):
        for j in range(i + 1, len(pads)):
            p1 = pads[i]
            p2 = pads[j]
            if getattr(p1, "component", None) is getattr(p2, "component", None):
                continue
            dx = p1.x - p2.x
            dy = p1.y - p2.y
            center_dist = math.hypot(dx, dy)
            clearance = center_dist - (max(p1.w, p1.h) / 2) - (max(p2.w, p2.h) / 2)
            if clearance < min_clearance:
                warnings.append(
                    f"Pad clearance between {p1.name} and {p2.name} is {clearance:.3f}mm; minimum {min_clearance}mm"
                )

    return warnings
