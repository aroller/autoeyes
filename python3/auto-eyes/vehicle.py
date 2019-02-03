import typing

from actor import Actor
from communicator import Communicator


class Vehicle:
    """Represents the autonomous vehicle communicating with actors"""

    def __init__(self, communicators: typing.List[Communicator]):
        """The actors currently seen, keyed by actor_id."""
        self._actors = {}
        self._communicators = communicators

    def sees(self, actor: Actor) -> Actor:
        """To confirm that the vehicle sees the actor at the location given."""
        actor_previous = None
        if actor.actor_id in self._actors:
            actor_previous = self._actors[actor.actor_id]

        self._actors[actor.actor_id] = actor
        for communicator in self._communicators:
            communicator.acknowledge_existence(actor)
        return actor_previous

    def no_longer_sees(self, actor_id: str) -> bool:
        """Removes the actor from the list since it is no longer seen. Returns true if it was found, otherwise false"""
        if actor_id in self.actors:
            del self.actors[actor_id]
            return True
        else:
            return False

    def clear(self):
        """Cleans up resources for all communicators and forgets all actors."""
        self._actors = {}
        for communicator in self._communicators:
            communicator.clear()

    @property
    def actors(self):
        """Provides actors currently seen, keyed by the actor_id"""
        return self._actors

    @property
    def communicators(self):
        return self._communicators
