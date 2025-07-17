class Zone:
    """Represents a filled copper area on a given layer."""

    def __init__(self, net=None, layer="GBL"):
        self.net = net
        self.layer = layer
