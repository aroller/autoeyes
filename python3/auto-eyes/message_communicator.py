from overrides import overrides

from api_model import ApiModel
from communicator import Communicator
from actor import Actor, Urgency


class MessageCommunicator(Communicator, ApiModel):
    """Communicator that formats a message returning basic state information.
       Useful for debugging or simple demonstration.
    """

    @overrides
    def sees(self, actor: Actor, previous_actor: Actor = None):
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

        message = "Actor `{actor_id}` at bearing {bearing} {modal_verb} {action}{direction}.".format(
            actor_id=actor.actor_id,
            bearing=actor.bearing,
            modal_verb=modal_verb,
            action=actor.action.value,
            direction=direction_message)
        print(message)
        return message

    @overrides
    def no_longer_sees(self, actor: Actor):
        super().no_longer_sees(actor)
        print('No longer sees {}'.format(actor.actor_id))

    def clear(self):
        super().clear()
        print("clearing all actors")

    def api_json(self):
        return {
            "messages": "no longer stateful"
        }
