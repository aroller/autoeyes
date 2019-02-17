import unittest

from colour import Color

from led_strip_controller import LedStripController


class LedStripControllerTest(unittest.TestCase):

    def test_clear_pixel(self):
        controller = LedStripController(3)
        index = 2
        color = Color('red')
        controller.pixel_color(index, color)
        controller.show()
        pixel = controller.strip.pixel_at(index)
        self.assertEqual(pixel.color.get_hex(), color.get_hex())
        controller.clear_pixel(index)
        controller.show()
        self.assertEqual(pixel.color.get_hex(), color.get_hex(), "original reference should remain unchanged")
        pixel_after_change = controller.strip.pixel_at(index)
        self.assertIsNone(pixel_after_change.color, "latest retrieval should represent state change")
