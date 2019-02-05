from colour import Color

from api_model import ApiModel


class Pixel(ApiModel):
    """Represents a single light on an LED Strip. Mutable"""

    def __init__(self,
                 index: int,
                 color: Color = None):
        self.index = index
        self.color = color

    def clear(self):
        """ Resets all fields, besides index, to None"""
        self.color = None

    def api_json(self):
        json = {
            "index": self.index,
        }
        if self.color is not None:
            json["color"] = self.color.get_hex()
        return json
