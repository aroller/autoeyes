from actor import Actor
from target import Target


class Vehicle:
    """Represents the autonomous vehicle communicating with actors"""

    def __init__(self):
        self._actors = {}
        """The actors currently seen, keyed by actor_id."""

    def sees(self, actor: Actor):
        """To confirm that the vehicle sees the actor at the location given."""
        self._actors[actor.actor_id] = actor

    def no_longer_sees(self, actor_id:str)-> bool:
        """Removes the actor from the list since it is no longer seen. Returns true if it was found, otherwise false"""
        if actor_id in self.actors():
            del self.actors()[actor_id]
            return True
        else:
            return False

    def actors(self):
        """Provides actors currently seen, keyed by the actor_id"""
        return self._actors
