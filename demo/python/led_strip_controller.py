from colour import Color


class LedStripController:
    """Modifies the LED strips in batches using the mutation methods that are applied by calling show().

    Based on the rpi_ws281x implementation of the NeoPixel and a simple wrapper for it, but portable.
    The controller uses a batch approach modifying all attributes as desired and then calling show
    to emit all changes at once.

    The controller has no relation to the application logic
    nor maintains any state beyond what can be seen by the led strip.

    Subclasses should override to modify
    the real world strip, but may call super method to print out state if desired.

    This default implementation allows testing and demonstration on dev enviroments where the raspberry pi led strip
    will not operate.
    """

    def __init__(self, pixel_count: int):
        self._pixel_count = pixel_count

    def clear_pixel(self, index: int):
        """Turn off the pixel"""
        print('clearing pixel at {}'.format(index))

    def pixel_color(self, index: int, color: Color):
        """Assigns a color to a specific pixel
            Parameters
            ----------
            index : int
                The index to the pixel starting at 0 at one end and increasing sequentially by 1 to the number of pixels.
            color: Color
                The color to be set to the pixel identified
        """
        color_value = color.get_hex() if color is not None else "off"
        print("setting color at {index} to {color}".format(index=index, color=color_value))

    def show(self):
        """
        Commits the batch of changes queued since the previous call to show.
        """
        print("calling show")

    def clear(self):
        """Clears all pixels"""
        for i in range(self._pixel_count):
            self.clear_pixel(i)

    @property
    def pixel_count(self):
        return self._pixel_count
