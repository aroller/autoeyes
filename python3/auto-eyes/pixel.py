from colour import Color

from api_model import ApiModel


class Pixel(ApiModel):
    """Represents a single light on an LED Strip. Immutable"""

    def __init__(self,
                 index: int,
                 color: Color = None):
        self._index = index
        self._color = color

    @property
    def index(self):
        return self._index

    @property
    def color(self):
        return self._color

    def clear(self):
        """Clears all properties of the pixel keeping the index"""
        return Pixel(index=self.index)

    def with_color(self, color: Color):
        """Creates a new pixel at the same index with color"""
        return Pixel(index=self.index, color=color)

    def api_json(self):
        return {
            "index": self.index,
            "color": self.color.get_hex()
        }

