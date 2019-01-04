from communicator import Communicator
from target import Target


class PrintCommunicator(Communicator):
    """Communicator that prints messages to standard out.  Mostly useful for debugging and demonstration."""

    def acknowledge_existence(self, target:Target):
        print("Target {} is at {}.".format(target.actor.actor_id,target.bearing))
