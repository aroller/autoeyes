from colour import Color

from pixel import Pixel


class LedStrip:
    """Mutable Data object representing the state of the led strip that contains a row of pixels"""

    def __init__(self, pixel_count: int):
        self._pixels = []
        for index in range(pixel_count):
            self._pixels.append(Pixel(index))

    @property
    def pixel_count(self):
        """The number of pixels in the entire LED strip, regardless of state"""
        return len(self._pixels)

    def pixel_at(self, index: int):
        return self._pixels[index]
