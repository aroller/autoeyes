import unittest
from api import *


class ApiTest(unittest.TestCase):

    def test_put_adds_actors(self):
        put_actor('a', 3.0)
        actors = list_actors()
        self.assertIsNotNone(actors)
        self.assertEqual(len(actors), 1)


if __name__ == '__main__':
    unittest.main()
