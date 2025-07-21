from typing import Callable
from ..Component import Component

from ..__init__ import Footprint

from .c0603 import apply as _c0603
from .tactile_switch import apply as _tactile_switch
from .header_1x5 import apply as _header_1x5
from .sop16 import apply as _sop16
from .sot223 import apply as _sot223
from .usb_c_cutout import apply as _usb_c_cutout
from .esp32_wroom import apply as _esp32_wroom
from .hdmi import apply as _hdmi


_MAPPING = {
    Footprint.C0603.value: _c0603,
    Footprint.TACTILE_SWITCH.value: _tactile_switch,
    Footprint.HEADER_1x5.value: _header_1x5,
    Footprint.SOP16.value: _sop16,
    Footprint.SOT223.value: _sot223,
    Footprint.USB_C_CUTOUT.value: _usb_c_cutout,
    Footprint.ESP32_WROOM.value: _esp32_wroom,
    "HDMI": _hdmi,
}


def get_footprint(name: str) -> Callable[[Component], None]:
    try:
        return _MAPPING[name]
    except KeyError:
        raise ValueError(f"Unknown footprint: {name}")
