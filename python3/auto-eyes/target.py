from actor import Actor


class Target:
    """
    The details relating to the location of an Actor in relation to a Vehicle.

    """

    def __init__(self, actor: Actor, bearing: float):
        self._bearing = bearing
        self._actor = actor

    @property
    def actor(self):
        return self._actor

    @property
    def bearing(self):
        return self._bearing
