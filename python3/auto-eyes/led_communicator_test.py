import unittest

from colour import Color
from overrides import overrides

from actor import Actor, Action
from led_communicator import LedCommunicator, ActionColorFilter
from led_strip_controller import LedStripController
from message_communicator import MessageCommunicator

PIXEL_COUNT = 360  # easy for 1:1 ratio testing
PIXELS_PER_ACTOR = 5
COLOR_FOR_ACTOR = ActionColorFilter().color_for_action(Action.SEEN)


class LedCommunicatorTest(unittest.TestCase):

    def __init__(self, method_name):
        super().__init__(methodName=method_name)
        self._communicator = LedCommunicator(
            LedStripController(pixel_count=PIXEL_COUNT), pixels_per_actor=PIXELS_PER_ACTOR)

    @property
    def communicator(self):
        return self._communicator

    def test_180_degrees_is_pixel_180(self):
        self.assertEqual(self.communicator._pixel_at_bearing(180), 180)

    def test_360_degrees_is_pixel_0(self):
        self.assertEqual(self.communicator._pixel_at_bearing(360), 0)

    def test_0_degrees_is_pixel_0(self):
        self.assertEqual(self.communicator._pixel_at_bearing(0), 0)

    def test_negative_1_degrees_is_pixel_359(self):
        self.assertEqual(self.communicator._pixel_at_bearing(-1), 359)

    def test_pixel_0_normalizes_to_0(self):
        self.assertEqual(self.communicator._normalized_pixel_index(0), 0)

    def test_pixel_neg_1_normalizes_to_359(self):
        self.assertEqual(self.communicator._normalized_pixel_index(-1), 359)

    def test_pixel_360_normalizes_to_0(self):
        self.assertEqual(self.communicator._normalized_pixel_index(360), 0)

    def test_pixels_for_actor_at_180(self):
        actor = Actor(actor_id='b', bearing=180)
        strip = self.communicator.sees(actor)
        # 5 pixels per actor
        self.assertEqual(None, strip.pixel_at(177).color)
        self.assertEqual(COLOR_FOR_ACTOR, strip.pixel_at(178).color)
        self.assertEqual(COLOR_FOR_ACTOR, strip.pixel_at(179).color)
        self.assertEqual(COLOR_FOR_ACTOR, strip.pixel_at(180).color)
        self.assertEqual(COLOR_FOR_ACTOR, strip.pixel_at(181).color)
        self.assertEqual(COLOR_FOR_ACTOR, strip.pixel_at(182).color)
        self.assertEqual(None, strip.pixel_at(183).color)

    def test_pixels_for_actor_at_0(self):
        actor = Actor(actor_id='c', bearing=0)
        strip = self.communicator.sees(actor)
        # 5 pixels per actor
        self.assertEqual(None, strip.pixel_at(357).color)
        self.assertEqual(COLOR_FOR_ACTOR, strip.pixel_at(358).color)
        self.assertEqual(COLOR_FOR_ACTOR, strip.pixel_at(359).color)
        self.assertEqual(COLOR_FOR_ACTOR, strip.pixel_at(0).color)
        self.assertEqual(COLOR_FOR_ACTOR, strip.pixel_at(1).color)
        self.assertEqual(COLOR_FOR_ACTOR, strip.pixel_at(2).color)
        self.assertEqual(None, strip.pixel_at(3).color)

    def test_sees_actor_pixels_set(self):
        actor_id = 'd'
        actor = Actor(actor_id=actor_id, bearing=100.0)
        self.communicator.sees(actor=actor)
        self.assertIn(actor_id, self.communicator._actor_pixels)

    def test_no_longer_sees_actor_pixels_set(self):
        actor_id = 'd'
        actor = Actor(actor_id=actor_id, bearing=100.0)
        self.communicator.sees(actor=actor)
        self.communicator.no_longer_sees(actor_id)
        self.assertNotIn(actor_id, self.communicator._actor_pixels)
        # TODO: confirm controller is called.


if __name__ == '__main__':
    unittest.main()
