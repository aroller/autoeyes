import colour
from overrides import overrides
from rpi_ws281x import *
import time

from led_strip_controller import LedStripController

LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
COLOR_FOR_OFF=colour.Color('black')

class RpiWs281xLedStripController(LedStripController):

    def __init__(self, pixel_count: int):
        super().__init__(pixel_count)
        # Create NeoPixel object with appropriate configuration.
        self._strip = Adafruit_NeoPixel(pixel_count, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS,
                                        LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        self._strip.begin()

    @overrides
    def show(self):
        self._strip.show()

    @overrides
    def clear_pixel(self, index: int):
        self.pixel_color(index=index, color=COLOR_FOR_OFF)

    @overrides
    def pixel_color(self, index: int, color: colour.Color):
        if color is None:
            color = COLOR_FOR_OFF
        ws281x_color = rpi_ws281x.Color(rgb_to_int(color.get_red()), rgb_to_int(color.get_green()), rgb_to_int(color.get_blue()))
        self._strip.setPixelColor(index, ws281x_color)


def rgb_to_int(rgb):
    return int(rgb * 255)
