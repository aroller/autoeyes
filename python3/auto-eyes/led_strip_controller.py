from copy import deepcopy

from colour import Color

from led_strip import LedStrip
from pixel import Pixel


class LedStripController:
    """Modifies the LED strips in batches using the mutation methods that are applied by calling show().

    Based on the rpi_ws281x implementation of the NeoPixel and a simple wrapper for it, but portable.
    The controller uses a batch approach modifying all attributes as desired and then calling show to emit all changes at once.

    The controller has
     
     

     no relation to the application logic nor maintains any state beyond what can be seen by the led strip.

    The state can be seen in the LedStrip objects maintained by this class queued and shown.  The show method moves
    pending changes from queued to shown.

    Subclasses should override to modify
    the real world strip, but must always call super method to maintain the LedStrip state.
    """

    def __init__(self, pixel_count: int):
        self._shown = LedStrip(pixel_count)  # current state of the led strip

    def show(self, pixels) -> LedStrip:
        """
        Commits the batch of changes queued since the previous call to show.
        :return: LedStrip currently shown
        """
        if isinstance(pixels, Pixel):
            pixels = [Pixel]
        self._shown = self._shown.set_pixels(pixels)
        return self._shown

    def clear(self):
        """Clears all pixels"""
        return self._shown.clear()

    @property
    def strip(self) -> LedStrip:
        """The LED strip currently shown"""
        return self._shown
