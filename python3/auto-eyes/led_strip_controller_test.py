import unittest

from colour import Color

from led_strip_controller import LedStripController
from pixel import Pixel


class LedStripControllerTest(unittest.TestCase):

    def test_set_pixel(self):
        controller = LedStripController(3)
        index = 2
        color = Color('red')
        controller.show([Pixel(index, color)])
        pixel = controller.strip.pixel_at(index)
        self.assertEqual(pixel.color.get_hex(), color.get_hex())

    def test_clear_pixels(self):
        controller = LedStripController(3)
        strip_showing_one = controller.show(Pixel(1, Color('blue')))
        strip_showing_none = controller.clear()
        self.assertNotEqual(len(strip_showing_none.pixels), len(strip_showing_one.pixels), "strips are immutable")
        self.assertEqual(0, len(strip_showing_none.pixels))
