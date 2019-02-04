from colour import Color

from animation import HasAnimation
from api_model import ApiModelSerializer
from communicator import Communicator
from actor import Actor, Action
from led_strip import LedStrip
from time import sleep

from led_strip_controller import LedStripController
from pixel import Pixel

FULL_CIRCLE_DEGREES = 360


class LedCommunicator(Communicator, HasAnimation):
    """
    Applies an LED Strip of pixels into an ellipse for 360 degree communication translating
    from application terms of actors in a scene to simple light terminology for pixel details
    like color, brightness and any animation necessary.
    """

    def __init__(self, controller: LedStripController,
                 pixels_per_actor: int = 5,
                 color_for_seen=Color('white'),
                 color_for_moving=Color('green'),
                 color_for_slowing=Color("#ffbf00"),  # amber
                 color_for_stopped=Color('red'),
                 ):
        self._controller = controller
        self._pixel_count = controller.strip.pixel_count
        self._pixels_per_actor = pixels_per_actor
        self._action_color = {
            Action.SEEN: color_for_seen,
            Action.MOVING: color_for_moving,
            Action.SLOWING: color_for_slowing,
            Action.STOPPED: color_for_stopped,
        }
        # map keyed by actor id keeping track of pixels
        self._actor_strip = {}

    def sees(self, actor: Actor) -> LedStrip:
        """
        `I See You` and `I'm watching you` scenario letting a human know the AV can see the actor and is watching.
        :param actor: the target that is seen
        :return: LedStrip currently shown
        """

        updated_pixels = []
        # first clear existing pixels, then set new and show in same batch to avoid race
        if actor.actor_id in self._actor_strip:
            previous_pixels = self._actor_strip[actor.actor_id].pixels
            for pixel in previous_pixels:
                updated_pixels.append(pixel.clear())

        # represent the actor around the center pixel
        middle_pixel = self._pixel_at_bearing(actor.bearing)
        additional_pixels = int(self._pixels_per_actor / 2)
        start_pixel = middle_pixel - additional_pixels
        end_pixel = middle_pixel + additional_pixels

        for i in range(start_pixel, end_pixel + 1):
            pixel_index = self._normalized_pixel_index(i)
            action_color = self._action_color[actor.action]
            pixel = Pixel(index=pixel_index, color=action_color)
            updated_pixels.append(pixel)

        # keep record of the current shown for hiding in the future
        self._actor_strip[actor.actor_id] = LedStrip(self._pixel_count).set_pixels(updated_pixels)

        # hide the old, show the new in the same commit
        return self._controller.show(updated_pixels)

    def no_longer_sees(self, actor_id: str) -> LedStrip:
        super().no_longer_sees(actor_id)
        strip = self._actor_strip.pop(actor_id, None)
        cleared_pixels = []
        if strip is not None:
            # FIXME: this will clobber another if they share pixels
            for pixel in strip.pixels:
                cleared_pixels.append(pixel.clear())
        return self._controller.show(cleared_pixels)

    def clear(self):
        super().clear()
        self._controller.clear()

    def welcome_light_show(self):
        """Light show demonstrating the wake up sequence to confirm system is up and grab attention."""
        actor_id = 'wake-up'
        for i in range(FULL_CIRCLE_DEGREES):
            self.sees(Actor(actor_id=actor_id, bearing=i))
            sleep(0.005)
        sleep(1.0)
        self.no_longer_sees(actor_id)

    def animate(self, time: float):
        pass

    def api_json(self):
        return {
            "pixelCount": self._pixel_count,
            "actorPixels": ApiModelSerializer.to_json(self._actor_strip)
        }

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
