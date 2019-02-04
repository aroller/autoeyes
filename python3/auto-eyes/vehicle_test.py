import unittest
import math

from message_communicator import MessageCommunicator
from target import Target
from actor import Actor

from vehicle import Vehicle

actor_1_id = "a"
actor_1 = Actor(actor_1_id, math.pi)


class VehicleTest(unittest.TestCase):

    def test_sees_actor(self):
        vehicle_1 = self.vehicle()
        vehicle_1.sees(actor_1)
        self.assertEqual(vehicle_1.actors[actor_1.actor_id], actor_1)

    def vehicle(self):
        return Vehicle([MessageCommunicator()])

    def test_doesnt_see_actor(self):
        vehicle_1 = self.vehicle()
        self.assertNotIn(actor_1.actor_id, vehicle_1.actors)

    def test_no_longer_sees(self):
        vehicle_1 = self.vehicle()
        self.assertFalse(vehicle_1.no_longer_sees(actor_1_id), "is not yet seen")
        vehicle_1.sees(actor_1)
        self.assertTrue(vehicle_1.no_longer_sees(actor_1_id), "should currently be seen")
        self.assertFalse(vehicle_1.no_longer_sees(actor_1_id), "should have been removed already")


if __name__ == '__main__':
    unittest.main()
