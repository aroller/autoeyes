import unittest

from colour import Color

from actor import Actor
from communicator_test import CommunicatorTest
from led_communicator import LedCommunicator
from led_strip_controller import LedStripController
from message_communicator import MessageCommunicator

PIXEL_COUNT = 360  # easy for 1:1 ratio testing
PIXELS_PER_ACTOR = 5
COLOR_FOR_ACTOR = Color('purple')


class LedCommunicatorTest(CommunicatorTest, unittest.TestCase):

    @property
    def communicator(self):
        return LedCommunicator(LedStripController(pixel_count=PIXEL_COUNT), pixels_per_actor=PIXELS_PER_ACTOR,
                               color_for_seen=COLOR_FOR_ACTOR)

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
        strip = self.communicator.acknowledge_existence(actor)
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
        strip = self.communicator.acknowledge_existence(actor)
        # 5 pixels per actor
        self.assertEqual(None, strip.pixel_at(357).color)
        self.assertEqual(COLOR_FOR_ACTOR, strip.pixel_at(358).color)
        self.assertEqual(COLOR_FOR_ACTOR, strip.pixel_at(359).color)
        self.assertEqual(COLOR_FOR_ACTOR, strip.pixel_at(0).color)
        self.assertEqual(COLOR_FOR_ACTOR, strip.pixel_at(1).color)
        self.assertEqual(COLOR_FOR_ACTOR, strip.pixel_at(2).color)
        self.assertEqual(None, strip.pixel_at(3).color)


if __name__ == '__main__':
    unittest.main()
