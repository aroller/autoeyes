import unittest

from colour import Color

from actor import Actor, Direction
from led_communicator import DirectionFilter, UrgencyColorFilter

colors5 = [Color('red'), Color('red'), Color('red'), Color('red'), Color('red')]
colors4 = [Color('red'), Color('red'), Color('red'), Color('red'), None]
colors3 = [Color('red'), Color('red'), Color('red'), None, None]
colors2 = [Color('red'), Color('red'), None, None, None]
colors1 = [Color('red'), None, None, None, None]
direction_filter = DirectionFilter(urgency_filter=UrgencyColorFilter(),
                                   seconds_per_sequence_for_no_urgency=1,
                                   pixels_per_actor=5)


class LedCommunicatorDirectionFilterTest(unittest.TestCase):

    def test_no_direction_returns_unchanged(self):
        actor = Actor(actor_id='a', bearing=33)
        colors = colors5
        filtered_colors = direction_filter.apply(actor=actor, colors=colors, call_time=0)
        self.assertEqual(colors, filtered_colors)

    def test_right_sequence_with_no_urgency(self):
        actor = Actor(actor_id='a', bearing=33, direction=Direction.RIGHT)
        call_time = 0
        self.assertEqual(colors1, direction_filter.apply(actor=actor, colors=colors5, call_time=call_time + 0))
        self.assertEqual(colors2, direction_filter.apply(actor=actor, colors=colors5, call_time=call_time + .2))
        self.assertEqual(colors3, direction_filter.apply(actor=actor, colors=colors5, call_time=call_time + .4))
        self.assertEqual(colors4, direction_filter.apply(actor=actor, colors=colors5, call_time=call_time + .6))
        self.assertEqual(colors5, direction_filter.apply(actor=actor, colors=colors5, call_time=call_time + .8))
        self.assertEqual(colors5, direction_filter.apply(actor=actor, colors=colors5, call_time=call_time + 0.99))
        self.assertEqual(colors1, direction_filter.apply(actor=actor, colors=colors5, call_time=call_time + 1.0))
        self.assertEqual(colors2, direction_filter.apply(actor=actor, colors=colors5, call_time=call_time + 1.2))
        self.assertEqual(colors3, direction_filter.apply(actor=actor, colors=colors5, call_time=call_time + 1.4))
        self.assertEqual(colors4, direction_filter.apply(actor=actor, colors=colors5, call_time=call_time + 1.6))
        self.assertEqual(colors5, direction_filter.apply(actor=actor, colors=colors5, call_time=call_time + 1.8))
        self.assertEqual(colors5, direction_filter.apply(actor=actor, colors=colors5, call_time=call_time + 1.99))
        self.assertEqual(colors1, direction_filter.apply(actor=actor, colors=colors5, call_time=call_time + 2))
