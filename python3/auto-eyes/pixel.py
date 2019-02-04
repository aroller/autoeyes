from colour import Color


class Pixel:
    """Represents a single light on an LED Strip. Mutable"""

    def __init__(self,
                 index: int,
                 color: Color = None):
        self.index = index
        self.color = color

    def clear(self):
        """ Resets all fields, besides index, to None"""
        self.color = None
