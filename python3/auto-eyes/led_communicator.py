from abc import ABCMeta, abstractmethod

from colour import Color

from animation import HasAnimation
from communicator import Communicator
from actor import Actor, Action, Urgency
from led_strip import LedStrip
from time import sleep, time

from led_strip_controller import LedStripController
from utils import min_filtered_none

FULL_CIRCLE_DEGREES = 360


class LedCommunicator(Communicator, HasAnimation):
    """
    Applies an LED Strip of pixels into an ellipse for 360 degree communication translating
    from application terms of actors in a scene to simple light terminology for pixel details
    like color, brightness and any animation necessary.
    """

    def __init__(self, controller: LedStripController,
                 pixels_per_actor: int = 5):
        self._controller = controller
        self._pixel_count = controller.pixel_count
        self._pixels_per_actor = pixels_per_actor
        # order matters since filters are applied in ascending order
        self._filters = [ActionColorFilter(), UrgencyColorFilter()]

    def sees(self, actor: Actor, previous_actor: Actor = None):
        call_time = time()
        return self._show_actor(actor=actor, previous_actor=previous_actor, call_time=call_time)

    def _show_actor(self, actor: Actor, call_time, previous_actor: Actor = None):
        # first clear existing pixels, then set new and show in same batch to avoid race
        if previous_actor is not None:
            previous_pixel_indexes = self._pixel_indexes_for_actor(previous_actor)
            for index in previous_pixel_indexes:
                self._controller.clear_pixel(index)
        current_pixel_indexes = self._pixel_indexes_for_actor(actor)
        seconds_til_refresh = None
        for pixel_index in current_pixel_indexes:
            # each pixel may have it's own color filtered for animation (Direction, for example)
            color = None
            for actor_filter in self._filters:
                color = actor_filter.apply(actor=actor, color=color, call_time=call_time)
                seconds_til_refresh = self.seconds_til_refresh_for_filter(actor, actor_filter, seconds_til_refresh)

            self._controller.pixel_color(pixel_index, color)
        self._controller.show()
        return seconds_til_refresh

    @staticmethod
    def seconds_til_refresh_for_filter(actor, actor_filter, seconds_til_refresh):
        """Requests the minimum refresh time for the filter and the actor"""
        if 'seconds_til_refresh' in dir(actor_filter):
            seconds_for_filter = actor_filter.seconds_til_refresh(actor)
            if seconds_for_filter is not None:
                if seconds_til_refresh is None:
                    seconds_til_refresh = seconds_for_filter
                else:
                    seconds_til_refresh = min(seconds_til_refresh, seconds_for_filter)
        return seconds_til_refresh

    def no_longer_sees(self, actor: Actor) -> LedStrip:
        super().no_longer_sees(actor)
        pixel_indexes = self._pixel_indexes_for_actor(actor)
        for index in pixel_indexes:
            # FIXME: this will clobber another if they share pixels
            self._controller.clear_pixel(index)
        return self._controller.show()

    def clear(self):
        super().clear()
        self._controller.clear()

    def welcome_light_show(self):
        """Light show demonstrating the wake up sequence to confirm system is up and grab attention."""
        actor_id = 'wake-up'
        i = 0
        previous_actor = None
        actor = None
        while i < FULL_CIRCLE_DEGREES:
            actor = Actor(actor_id=actor_id, bearing=i)
            self.sees(actor=actor, previous_actor=previous_actor)
            previous_actor = actor
            sleep(0.005)
            i = i + 10
        sleep(1.0)
        self.no_longer_sees(actor)

    def animate(self, actors: dict, call_time: float) -> float:
        seconds_til_refresh = None
        for actor in actors.values():
            seconds_til_refresh_for_actor = self._show_actor(actor=actor, call_time=call_time)
            refresh_rates = [seconds_til_refresh, seconds_til_refresh_for_actor]
            seconds_til_refresh = min_filtered_none(refresh_rates)
        return seconds_til_refresh

    def _pixel_indexes_for_actor(self, actor: Actor):
        pixel_indexes = []
        # represent the actor around the center pixel
        middle_pixel = self._pixel_at_bearing(actor.bearing)
        additional_pixels = int(self._pixels_per_actor / 2)
        start_pixel = middle_pixel - additional_pixels
        end_pixel = middle_pixel + additional_pixels
        for i in range(start_pixel, end_pixel + 1):
            pixel_index = self._normalized_pixel_index(i)
            pixel_indexes.append(pixel_index)
        return pixel_indexes

    def _normalized_pixel_index(self, index: int):
        """indexes start at 0 and go to one less than count.  if outside that range, make it fit within the range
         by adding or subtracting count to continue around the circle"""
        if index >= self._pixel_count:
            return index - self._pixel_count  # beyond the index of 299 for 300 count so subtract making 300-300=0
        elif index < 0:
            return index + self._pixel_count  # subtracts index from count so 300 count at -1 is 299 index
        else:
            return index

    def _pixel_at_bearing(self, bearing: float) -> int:
        """Given a bearing, this will return the nearest pixel index."""
        if bearing >= FULL_CIRCLE_DEGREES:
            bearing = bearing - FULL_CIRCLE_DEGREES
        elif bearing < 0:
            bearing = bearing + FULL_CIRCLE_DEGREES
        return int(self._pixel_count * (bearing / FULL_CIRCLE_DEGREES))


class ActorColorFilter(metaclass=ABCMeta):
    """Interface for changing the color based on the actor properties."""

    @abstractmethod
    def apply(self, actor: Actor, color: Color, call_time: float = None):
        pass


class ActionColorFilter(ActorColorFilter):

    def __init__(self,
                 color_for_seen=Color('white'),
                 color_for_moving=Color('green'),
                 color_for_slowing=Color('#ffbf00'),  # amber
                 color_for_stopped=Color('red'), ):
        super().__init__()
        self._action_color = {
            Action.SEEN: color_for_seen,
            Action.MOVING: color_for_moving,
            Action.SLOWING: color_for_slowing,
            Action.STOPPED: color_for_stopped,
        }

    def apply(self, actor: Actor, color: Color, call_time: float = None):
        if actor.action is not None:
            return self._action_color[actor.action]
        else:
            return None

    def color_for_action(self, action: Action):
        return self._action_color[action]


class UrgencyColorFilter(ActionColorFilter):

    def __init__(self,
                 flash_per_second_for_request=4,
                 flash_per_second_for_demand=8):
        super().__init__()
        self._seconds_per_flash_for_urgency = {
            Urgency.REQUEST: 1 / flash_per_second_for_request,
            Urgency.DEMAND: 1 / flash_per_second_for_demand
        }
        # FIXME: this should be stateless
        self._time_of_previous_flash_on = 0

    def seconds_til_refresh(self, actor: Actor):
        seconds = None
        if actor.urgency is not None:
            seconds = self._seconds_per_flash_for_urgency[actor.urgency]
        return seconds

    def apply(self, actor: Actor, color: Color, call_time: float = None):
        urgency = actor.urgency

        if urgency is None:  # no urgency, no flash
            urgency_color = color
        else:
            seconds_since_previous_on = call_time - self._time_of_previous_flash_on
            seconds_for_flash = self._seconds_per_flash_for_urgency[urgency]

            if seconds_since_previous_on < seconds_for_flash:
                urgency_color = None  # light is off
            else:
                # 2 x flash duration -> reset to off
                if seconds_since_previous_on >= 2 * seconds_for_flash:
                    self._time_of_previous_flash_on = call_time
                    urgency_color = None
                else:
                    urgency_color = color  # light is on

        return urgency_color
