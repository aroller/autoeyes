import unittest

from led_strip import LedStrip


class LedStripTest(unittest.TestCase):

    def test_pixels_created_during_construction(self):
        pixel_count = 20
        strip = LedStrip(pixel_count)
        self.assertEqual(strip.pixel_count, pixel_count)
        index = 10
        pixel = strip.pixel_at(index)
        self.assertEqual(pixel.index, index)
