from api_model import ApiModel
from enum import Enum


class Action(Enum):
    SEEN = "seen"
    """Existence is acknowledge, but intent is not determined nor recommended."""
    MOVING = "moving"
    """Acknowledge that the actor is not stationary and has an intent and the AV agrees the actor can move."""
    SLOWING = "slowing"
    """Mostly used to encourage an actor to slow down because a potential collision has been detected."""
    STOPPED = "stopped"
    """Acknowledge that the actor is not moving nor expected to move."""


class Direction(Enum):
    """Used to acknowledge or encourage an actor to move in a specific direction, relative to the vehicle."""
    RIGHT = "right"
    """Clockwise"""
    LEFT = "left"
    """Counterclockwise"""


class Actor(ApiModel):
    """
    Any human or humans outside of the Vehicle.  Typically pedestrians, bicyclists or other mobility users in the scene.
    
    """

    def __init__(self, actor_id: str, bearing: float,
                 action: Action = Action.SEEN,
                 direction: Direction = None):
        self._actor_id = actor_id
        self._bearing = bearing
        self._action = action
        self._direction = direction

    @property
    def actor_id(self) -> str:
        """A unique identifier, provided by the client, to uniquely identify this actor across calls."""
        return self._actor_id

    @property
    def bearing(self) -> float:
        """The degrees clockwise from the forward direction of a vehicle to the location of the actor."""
        return self._bearing

    @property
    def action(self) -> Action:
        """What the vehicle thinks the actor will be doing."""
        return self._action

    @property
    def direction(self):
        return self._direction

    def api_json(self):
        json = {
            "actorId": self.actor_id,
            "bearing": self.bearing,
            "action": self.action.value,
        }
        if self.direction is not None:
           json["direction"] = self.direction.value
        return json
