import unittest

from colour import Color

from pixel import Pixel


class PixelTest(unittest.TestCase):

    def test_clear_resets_color(self):
        color = Color('red')
        pixel_original = Pixel(0, color)
        pixel_modified = pixel_original.clear()
        self.assertIsNone(pixel_modified.color)
        self.assertEqual(color, pixel_original.color)

    def test_index_is_assigned_during_construction(self):
        index = 33
        pixel = Pixel(index)
        self.assertEqual(pixel.index, index)

    def test_index_is_unaffected_during_clear(self):
        index = 22
        pixel = Pixel(index)
        pixel.clear()
        self.assertEqual(pixel.index, index)
