from enum import Enum

from api_model import ApiModel


class Action(Enum):
    """What the vehicle expects or desires the actor to do."""
    SEEN = "seen"
    """Existence is acknowledged, but intent is not determined nor recommended."""
    MOVING = "moving"
    """Acknowledge that the actor is not stationary and has an intent and the AV agrees the actor can move."""
    SLOWING = "slowing"
    """Mostly used to encourage an actor to slow down because a potential collision has been detected."""
    STOPPED = "stopped"
    """Acknowledge that the actor is not moving nor expected to move."""


class Direction(Enum):
    """Used to acknowledge or encourage an actor to move in a specific direction,
    from the perspective of the vehicle."""
    RIGHT = "right"
    """Clockwise"""
    LEFT = "left"
    """Counterclockwise"""


class Urgency(Enum):
    """Identifies the level of importance for an actor to follow a desired action."""
    REQUEST = "request"
    """Acquires attention and politely asking for the requested action to be followed. 
        Example: Asking a ped to wait to cross in a crosswalk since the AV can finish up.
    """
    DEMAND = "demand"
    """Demonstrating authority that an action be followed.  Example: When a ped is jaywalking and in the AVs intent."""


DEFAULT_ACTION = Action.SEEN


class Actor(ApiModel):
    """
    Any human or humans outside of the Vehicle.  Typically pedestrians, bicyclists or other mobility users in the scene.
    
    """

    def __init__(self, actor_id: str, bearing: float,
                 action: Action = DEFAULT_ACTION,
                 direction: Direction = None,
                 urgency: Urgency = None,
                 time_seen: str = None):
        self._actor_id = actor_id
        self._bearing = bearing
        self._action = action
        self._direction = direction
        self._urgency = urgency
        self._time_seen = time_seen

        if self._action is None:
            self._action = DEFAULT_ACTION

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

    @property
    def urgency(self):
        return self._urgency

    @property
    def time_seen(self) -> str:
        """The time the actor was seen, in iso format.  Provided by the client, this helps with ensuring aynch calls
        are being handled in the proper order."""
        return self._time_seen

    def api_json(self):
        json = {
            "actorId": self.actor_id,
            "bearing": self.bearing,
            "action": self.action.value,
        }
        if self.urgency is not None:
            json["urgency"] = self.urgency.value
        if self.direction is not None:
            json["direction"] = self.direction.value
        if self.time_seen is not None:
            json["timeSeen"] = self._time_seen
        return json
