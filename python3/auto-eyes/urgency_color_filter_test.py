import unittest
from time import time

from colour import Color

from actor import Actor, Urgency
from led_communicator import UrgencyColorFilter, LedCommunicator

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

    def test_request_urgency_with_4_flashes_per_second(self):
        urgency_filter = UrgencyColorFilter(flash_per_second_for_request=4)
        actor_with_urgency = actor(Urgency.REQUEST)
        # start with even number at first
        call_time = 12343332
        self.assertIsNone(urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=call_time + 0),
                          "off at first")
        self.assertIsNone(urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=call_time + .24),
                          "still off for almost 1/4 second")
        self.assertEqual(given_color,
                         urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=call_time + 0.25),
                         "on at 1/4 second")
        self.assertEqual(given_color,
                         urgency_filter.apply(actor=actor_with_urgency, color=given_color,
                                              call_time=call_time + 0.4999),
                         "on at almost 1/2 second")
        self.assertIsNone(urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=call_time + 0.5),
                          "off again at 1/2 second")

    def test_request_with_real_time(self):
        duration = 1
        urgency_filter = UrgencyColorFilter(flash_per_second_for_request=duration)
        call_time = time()
        actor_with_urgency = actor(Urgency.REQUEST)
        self.assertIsNone(urgency_filter.apply(actor=actor_with_urgency, color=given_color, call_time=call_time),
                          "off at first")
        self.assertEqual(given_color,
                         urgency_filter.apply(actor=actor_with_urgency, color=given_color,
                                              call_time=call_time + duration),
                         "should be on")


class UrgencyFilterRefreshTest(unittest.TestCase):

    def __init__(self, method_name):
        super().__init__(method_name)
        self.flashes_per_second = 4.0
        self.actor_filter = UrgencyColorFilter(flash_per_second_for_request=self.flashes_per_second)
        self.request_urgency_refresh_seconds = 1 / self.flashes_per_second

    def test_seconds_til_refresh_for_none_given(self):
        refresh_seconds = LedCommunicator.seconds_til_refresh_for_filter(actor=actor(Urgency.REQUEST),
                                                                         actor_filter=self.actor_filter,
                                                                         seconds_til_refresh=None)
        self.assertEqual(self.request_urgency_refresh_seconds, refresh_seconds)

    def test_seconds_til_refresh_for_faster_given(self):
        given_is_small = self.request_urgency_refresh_seconds / 2
        refresh_seconds = LedCommunicator.seconds_til_refresh_for_filter(actor=actor(Urgency.REQUEST),
                                                                         actor_filter=self.actor_filter,
                                                                         seconds_til_refresh=given_is_small)
        self.assertEqual(given_is_small, refresh_seconds, "the smaller refresh rate given_is_small should be chosen")

    def test_seconds_til_refresh_for_slower_given(self):
        given_is_bigger = self.request_urgency_refresh_seconds * 2
        refresh_seconds = LedCommunicator.seconds_til_refresh_for_filter(actor=actor(Urgency.REQUEST),
                                                                         actor_filter=self.actor_filter,
                                                                         seconds_til_refresh=given_is_bigger)
        self.assertEqual(self.request_urgency_refresh_seconds, refresh_seconds,
                         "the smaller refresh rate calculated should be chosen")

    def test_seconds_til_refresh_is_none_for_no_urgency(self):
        refresh_seconds = LedCommunicator.seconds_til_refresh_for_filter(actor=actor(),
                                                                         actor_filter=self.actor_filter,
                                                                         seconds_til_refresh=None)
        self.assertEqual(None, refresh_seconds)

    def test_seconds_til_refresh_is_given_for_no_urgency(self):
        given = 5
        refresh_seconds = LedCommunicator.seconds_til_refresh_for_filter(actor=actor(),
                                                                         actor_filter=self.actor_filter,
                                                                         seconds_til_refresh=given)
        self.assertEqual(given, refresh_seconds)


def actor(urgency: Urgency = None):
    return Actor(actor_id="a", bearing=0, urgency=urgency)
