import typing

from actor import Actor
from animation import HasAnimation
from communicator import Communicator


class Vehicle:
    """Represents the autonomous vehicle communicating with actors"""

    def __init__(self, communicators: typing.List[Communicator]):
        """The actors currently seen, keyed by actor_id."""
        self._actors = {}
        self._communicators = communicators

    def sees(self, actor: Actor) -> Actor:
        """To confirm that the vehicle sees the actor at the location given."""
        actor_previous = self.actors.pop(actor.actor_id, None)
        self._actors[actor.actor_id] = actor
        for communicator in self._communicators:
            communicator.sees(actor=actor, previous_actor=actor_previous)
        return actor_previous

    def no_longer_sees(self, actor_id: str) -> bool:
        """Removes the actor from the list since it is no longer seen. Returns true if it was found, otherwise false"""
        actor = self.actors.pop(actor_id, None)
        if actor is not None:
            for communicator in self.communicators:
                communicator.no_longer_sees(actor=actor)
            return True
        else:
            return False

    def clear(self):
        """Cleans up resources for all communicators and forgets all actors."""
        self._actors = {}
        for communicator in self._communicators:
            communicator.clear()

    def animate(self, time: float):
        """Calls each Communicator that is HasAnimation so they may update as necessary."""
        for communicator in self._communicators:
            if isinstance(communicator, HasAnimation):
                communicator.animate(self.actors, time)

    @property
    def actors(self):
        """Provides actors currently seen, keyed by the actor_id"""
        return self._actors

    @property
    def communicators(self):
        return self._communicators
