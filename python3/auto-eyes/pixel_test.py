import unittest

from colour import Color

from pixel import Pixel


class PixelTest(unittest.TestCase):

    def test_clear_resets_color(self):
        pixel = Pixel(0)
        pixel.color = Color('red')
        pixel.clear()
        self.assertIsNone(pixel.color)

    def test_index_is_assigned_during_construction(self):
        index = 33
        pixel = Pixel(index)
        self.assertEqual(pixel.index, index)

    def test_index_is_unaffected_during_clear(self):
        index = 22
        pixel = Pixel(index)
        pixel.clear()
        self.assertEqual(pixel.index, index)
