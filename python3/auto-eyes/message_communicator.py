from api_model import ApiModel
from communicator import Communicator
from actor import Actor


class MessageCommunicator(Communicator, ApiModel):
    """Communicator that formats a message returning basic state information.
       Useful for debugging or simple demonstration.
    """

    def __init__(self):
        self._actor_messages = {}  # keyed by actor id

    def acknowledge_existence(self, actor: Actor):
        message = "Actor {} is at {}.".format(actor.actor_id, actor.bearing)
        self._actor_messages[actor.actor_id] = message
        return message

    def api_json(self):
        return {
            "messages": self._actor_messages
        }
