from .Pin import Pin
from .Pad import Pad
from .Component import Component
from .Via import Via
from .Graphic import Graphic
from .Board import Board
from .Zone import Zone
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
]
