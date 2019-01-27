from communicator import Communicator
from actor import Actor


class PrintCommunicator(Communicator):
    """Communicator that prints messages to standard out.  Mostly useful for debugging and demonstration."""

    def acknowledge_existence(self, actor:Actor):
        print("Actor {} is at {}.".format(actor.actor_id,actor.bearing))
