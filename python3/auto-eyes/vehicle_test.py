import unittest
import math
from target import Target
from actor import Actor

from vehicle import Vehicle


class VehicleTest(unittest.TestCase):
    def test_sees_actor(self):
        target = Target(Actor("a"), math.pi)
        Vehicle().sees(target)

if __name__ == '__main__':
    unittest.main()
