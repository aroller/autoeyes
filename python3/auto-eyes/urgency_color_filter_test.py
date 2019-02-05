import unittest
from time import time

from colour import Color

from actor import Actor, Urgency
from led_communicator import UrgencyColorFilter

given_color = Color('red')


class UrgencyColorFilterTest(unittest.TestCase):

    def test_no_urgency_returns_given_color(self):
        urgency_filter = UrgencyColorFilter()
        filtered_color = urgency_filter.apply(actor(), given_color)
        self.assertEqual(given_color, filtered_color)

    def test_request_urgency_flashes_for_1_second(self):
        urgency_filter = UrgencyColorFilter(flash_per_second_for_request=1)
        actor_with_urgency = actor(Urgency.REQUEST)
        self.assertIsNone(urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=0),
                          "off at first")
        self.assertIsNone(urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=.25),
                          "still off  at  1/4 second")
        self.assertIsNone(urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=.5),
                          "still off  at  1/2 second")
        self.assertIsNone(urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=.999),
                          "still off  almost 1 second")
        self.assertEqual(given_color,
                         urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=1.0),
                         "on at 1 second")
        self.assertEqual(given_color,
                         urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=1.999),
                         "on at almost 2 seconds")
        self.assertIsNone(urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=2.0),
                          "off again at 2 seconds")
        self.assertIsNone(urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=2.0),
                          "still off at almost 3 seconds")
        self.assertEqual(given_color,
                         urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=3.0),
                         "on again at 3 seconds")
        self.assertEqual(given_color,
                         urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=3.999),
                         "still on at almost 3 seconds")
        self.assertIsNone(urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=4.0),
                          "off again at 4 seconds")

    def test_request_with_real_time(self):
        duration = 1
        urgency_filter = UrgencyColorFilter(flash_per_second_for_request=duration)
        call_time = time()
        actor_with_urgency = actor(Urgency.REQUEST)
        self.assertIsNone(urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=call_time),
                          "off at first")
        self.assertEqual(given_color,
                         urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=call_time+duration),
                         "should be on")

def actor(urgency: Urgency = None):
    return Actor(actor_id="a", bearing=0, urgency=urgency)
