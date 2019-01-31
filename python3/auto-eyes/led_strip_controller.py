from copy import deepcopy

from colour import Color

from led_strip import LedStrip


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
        self._shown = LedStrip(pixel_count) # current state of the led strip
        self._future = LedStrip(pixel_count) # convenience of changing the shown + queued real time as they are applied

    def clear_pixel(self, index: int):
        self._future.pixel_at(index).clear()

    def pixel_color(self, index: int, color: Color):
        """Assigns a color to a specific pixel
            Parameters
            ----------
            index : int
                The index to the pixel starting at 0 at one end and increasing sequentially by 1 to the number of pixels.
            color: Color
                The color to be set to the pixel identified
        """
        self._future.pixel_at(index).color = color

    def show(self):
        """Commits the batch of changes queued since the previous call to show."""
        # possibly inefficient way to manage
        self._shown = deepcopy(self._future)

    @property
    def strip(self)-> LedStrip:
        """The LED strip currently shown"""
        return self._shown
