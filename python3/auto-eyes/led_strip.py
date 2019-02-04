from collections import ValuesView
from copy import deepcopy
from typing import List

from colour import Color

from api_model import ApiModel, ApiModelSerializer
from pixel import Pixel


class LedStrip(ApiModel):
    """Mutable Data object representing the state of the led strip that contains a row of pixels"""

    def __init__(self, pixel_count: int):
        self._pixels = {}
        self._pixel_count = pixel_count

    @property
    def pixel_count(self):
        """The number of pixels in the entire LED strip, regardless of state"""
        return self._pixel_count

    def pixel_at(self, index: int):
        if index < 0 or index >= self._pixel_count:
            raise ValueError("{index} is not in range(0,{max})".format(index=index, max=self.pixel_count))

        key = _pixel_index_key(index)
        if key in self._pixels:
            pixel = self._pixels[key]
        else:
            pixel = Pixel(index=index)
            # no need to assign yet because it lacks color or other properties
        return pixel

    def set_pixels(self, pixels):
        if isinstance(pixels, Pixel):
            pixels = [pixels]
        copy = deepcopy(self)
        for pixel in pixels:
            copy._pixels[_pixel_index_key(pixel.index)] = pixel
        return copy

    def clear(self):
        return LedStrip(pixel_count=self.pixel_count)

    @property
    def pixels(self) -> ValuesView:
        """Returns the list of pixels currently set"""
        return self._pixels.values()

    def api_json(self):
        return {
            "pixelCount": self._pixel_count,
            "pixels": ApiModelSerializer.to_json(self.pixels)

        }


def _pixel_index_key(index: int):
    return str(index)
