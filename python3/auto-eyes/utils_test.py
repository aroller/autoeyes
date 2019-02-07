import unittest

from utils import min_filtered_none


class MinWithNoneTest(unittest.TestCase):

    def test_none(self):
        actual = min_filtered_none([None])
        self.assertIsNone(actual)

    def test_nones(self):
        self.assertIsNone(min_filtered_none([None, None]))

    def test_with_one_and_none(self):
        self.assertEqual(1, min_filtered_none([1, None]))

    def test_with_no_parameter(self):
        self.assertIsNone(min_filtered_none())
