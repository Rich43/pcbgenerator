from .Pin import Pin
from .Pad import Pad
from .Component import Component
from .Via import Via
from .Graphic import Graphic
from .Board import Board
from .Zone import Zone
from .drc import check_board
from .circuits import (
    create_voltage_divider,
    create_led_indicator,
    create_rc_lowpass,
    create_bent_trace,
)

# Default symbolic layer names
TOP_SILK = "GTO"
BOTTOM_SILK = "GBO"

PCB = Board

from enum import Enum


class Layer(str, Enum):
    TOP_COPPER = "GTL"
    BOTTOM_COPPER = "GBL"
    TOP_SILK = TOP_SILK
    BOTTOM_SILK = BOTTOM_SILK


class Footprint(Enum):
    ESP32_WROOM = "ESP32_WROOM"
    SOP16 = "SOP16"
    SOT223 = "SOT223"
    USB_C_CUTOUT = "USB_C_CUTOUT"
    C0603 = "C0603"
    TACTILE_SWITCH = "TACTILE_SWITCH"
    HEADER_1x5 = "HEADER_1x5"


# Basic design rule parameters for common board configurations
LAYER_SERVICE_RULES = {
    "2 Layer Services": {
        "Minimum Clearance": "6mil (0.1524mm)",
        "Minimum track Width": "6mil (0.1524mm)",
        "Minimum Connection Width": "6mil (0.1524mm)",
        "Minimum Annular Ring": "5mil (0.127mm)",
        "Minimum Via Diameter": "20mil (0.508mm)",
        "Copper to hole clearance": "5mil (0.127mm)",
        "Minimum Through Hole": "10mil (0.254mm)",
        "Hole to hole clearance": "5mil (0.127mm)",
        "Minimum uVia diameter": "20mil (0.508mm)",
        "minimum uVia Hole": "10mil (0.254mm)",
        "Silkscreen Min Item Clearance": "user preference",
        "Silkscreen Min Text Height": "user preference",
        "Silkscreen Min Text Thickness": "5mil (0.127mm)",
    },
    "4 Layer": {
        "Minimum Clearance": "5mil (0.127mm)",
        "Minimum track Width": "5mil (0.127mm)",
        "Minimum Connection Width": "5mil (0.127mm)",
        "Minimum Annular Ring": "4mil (0.1016mm)",
        "Minimum Via Diameter": "18mil (0.4572mm)",
        "Copper to hole clearance": "5mil (0.127mm)",
        "Minimum Through Hole": "10mil (0.254mm)",
        "Hole to hole clearance": "5mil (0.127mm)",
        "Minimum uVia diameter": "18mil (0.4572mm)",
        "minimum uVia Hole": "10mil (0.254mm)",
        "Silkscreen Min Item Clearance": "any",
        "Silkscreen Min Text Height": "any",
        "Silkscreen Min Text Thickness": "5mil (0.127mm)",
    },
    "6 Layer": {
        "Minimum Clearance": "5mil (0.127mm)",
        "Minimum track Width": "5mil (0.127mm)",
        "Minimum Connection Width": "5mil (0.127mm)",
        "Minimum Annular Ring": "4mil (0.1016mm)",
        "Minimum Via Diameter": "16mil (0.4064mm)",
        "Copper to hole clearance": "5mil (0.127mm)",
        "Minimum Through Hole": "8mil (0.2032mm)",
        "Hole to hole clearance": "5mil (0.127mm)",
        "Minimum uVia diameter": "16mil (0.4064mm)",
        "minimum uVia Hole": "8mil (0.2032mm)",
        "Silkscreen Min Item Clearance": "any",
        "Silkscreen Min Text Height": "any",
        "Silkscreen Min Text Thickness": "5mil (0.127mm)",
    },
}


__all__ = [
    "Board",
    "PCB",
    "Component",
    "Pin",
    "Pad",
    "Via",
    "Zone",
    "Graphic",
    "Layer",
    "Footprint",
    "create_voltage_divider",
    "create_led_indicator",
    "create_rc_lowpass",
    "create_bent_trace",
    "TOP_SILK",
    "BOTTOM_SILK",
    "check_board",
    "LAYER_SERVICE_RULES",
]
