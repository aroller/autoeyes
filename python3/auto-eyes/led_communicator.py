from colour import Color

from communicator import Communicator
from actor import Actor

from led_strip_controller import LedStripController

PIXELS_PER_ACTOR = 5
COLOR_FOR_SEEN = Color('red')


class LedCommunicator(Communicator):
    """
    Applies an LED Strip of pixels into an ellipse for 360 degree communication translating
    from application terms of actors in a scene to simple light terminology for pixel details
    like color, brightness and any animation necessary.
    """

    def __init__(self, controller: LedStripController):
        self._controller = controller
        self._led_count = controller.strip.pixel_count
        # map keyed by actor id keeping track of pixels
        self._actor_pixels = {}

    def acknowledge_existence(self, actor: Actor):
        # first clear existing pixels, then set new and show in same batch to avoid race
        if actor.actor_id in self._actor_pixels:
            previous_pixels = self._actor_pixels[actor.actor_id]
            print("found previous pixels {previous_pixels}".format(previous_pixels=previous_pixels))
            for i in range(len(previous_pixels)):
                self._controller.clear_pixel(previous_pixels[i])
        else:
            print("{actor_id} not found in {ids}".format(actor_id=actor.actor_id, ids=self._actor_pixels.keys()))

        # represent the actor around the center pixel
        middle_pixel = self.pixel_at_bearing(actor.bearing)
        additional_pixels = int(PIXELS_PER_ACTOR / 2)
        start_pixel = middle_pixel - additional_pixels
        end_pixel = middle_pixel + additional_pixels
        current_pixel_indexes = []
        for i in range(start_pixel, end_pixel):
            pixel_index = self.normalized_pixel_index(i)
            current_pixel_indexes.append(pixel_index)
            self._controller.pixel_color(pixel_index, COLOR_FOR_SEEN)

        # hide the old, show the new in the same commit
        self._controller.show()

        # keep record of the current shown for hiding in the future
        self._actor_pixels[actor.actor_id] = current_pixel_indexes

    def normalized_pixel_index(self, index: int):
        """indexes start at 0 and go to one less than count.  if outside that range, make it fit within the range
         by adding or subtracting count to continue around the circle"""
        if index >= self._led_count:
            return index - self._led_count  # beyond the index of 299 for 300 count so subtract making 300-300=0
        elif index < 0:
            return index + self._led_count  # subtracts index from count so 300 count at -1 is 299 index
        else:
            return index

    def pixel_at_bearing(self, bearing: float) -> int:
        """Given a bearing, this will return the nearest pixel index."""
        if bearing >= 360:
            bearing = bearing - 360
        elif bearing < 0:
            bearing = bearing + 360
        return int(self._led_count * (bearing / 360.0))
