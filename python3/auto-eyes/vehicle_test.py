import unittest
import math
from time import time

from led_communicator import LedCommunicator
from led_strip_controller import LedStripController
from message_communicator import MessageCommunicator
from target import Target
from actor import Actor, Urgency

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

    def test_vehicle_does_not_animates_if_sees_urgency_with_unanimated_communicator(self):
        vehicle = self.vehicle()  # only message communicator
        vehicle.sees(Actor(actor_id=actor_1_id, bearing=20, urgency=Urgency.REQUEST))
        self.assertIsNone(vehicle.animate(time=time()))

    def test_vehicle_animates_if_sees_urgency_with_animated_communicator(self):
        vehicle = Vehicle([LedCommunicator(LedStripController(10))])
        vehicle.sees(Actor(actor_id=actor_1_id, bearing=20, urgency=Urgency.REQUEST))
        self.assertIsNotNone(vehicle.animate(time=time()))


if __name__ == '__main__':
    unittest.main()
