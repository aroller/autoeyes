import unittest
from unittest.mock import MagicMock

from colour import Color

from actor import Action, Actor
from led_communicator import LedCommunicator, ActionColorFilter
from led_strip_controller import LedStripController


class LedCommunicatorActionFilterTest(unittest.TestCase):

    def __init__(self, method_name):
        super().__init__(method_name)
        self.filter = ActionColorFilter()

    def test_seen_is_white(self):
        self.assertEqual(Color('white'), self.filter.color_for_action(Action.SEEN))

    def test_stopped_is_red(self):
        self.assertEqual(Color('red'), self.filter.color_for_action(Action.STOPPED))

    def test_slowing_is_amber(self):
        self.assertEqual(Color('#ffbf00'), self.filter.color_for_action(Action.SLOWING))

    def test_moving_is_green(self):
        self.assertEqual(Color('green'), self.filter.color_for_action(Action.MOVING))

    def test_communicator_sees_green(self):
        controller = LedStripController(10)
        controller.pixel_color = MagicMock()
        controller.show = MagicMock()
        self.communicator = LedCommunicator(controller)

        self.communicator.sees(Actor(actor_id='1', bearing=33, action=Action.STOPPED))
        controller.show.assert_called()
        controller.pixel_color.assert_called_with(2, Color('red'))
