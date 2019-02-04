from overrides import overrides

from api_model import ApiModel
from communicator import Communicator
from actor import Actor, Urgency


class MessageCommunicator(Communicator, ApiModel):
    """Communicator that formats a message returning basic state information.
       Useful for debugging or simple demonstration.
    """

    def __init__(self):
        self._actor_messages = {}  # keyed by actor id

    @overrides
    def sees(self, actor: Actor):
        super().sees(actor)

        if actor.direction is not None:
            direction_message = " to the {}".format(actor.direction.value)
        else:
            direction_message = ""

        if actor.urgency is not None:
            if actor.urgency == Urgency.REQUEST:
                modal_verb = "should be"
            elif actor.urgency == Urgency.DEMAND:
                modal_verb = "must be"
            else:
                raise ValueError("urgency {} not handled".format(actor.urgency))
        else:
            modal_verb = "is"

        message = "Actor `{}` at bearing {}° {} {}{}.".format(
            actor.actor_id,
            actor.bearing,
            modal_verb,
            actor.action.value,
            direction_message)
        self._actor_messages[actor.actor_id] = message
        return message

    @overrides
    def no_longer_sees(self, actor_id: str):
        super().no_longer_sees(actor_id)
        self._actor_messages.pop(actor_id, None)

    def clear(self):
        super().clear()
        self._actor_messages = {}

    def api_json(self):
        return {
            "messages": self._actor_messages
        }
