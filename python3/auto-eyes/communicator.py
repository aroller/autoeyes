from abc import ABCMeta, abstractmethod

from actor import Actor
from api_model import ApiModel


class Communicator(ApiModel, metaclass=ABCMeta):
    """
    Sends messages from the Vehicle to Actors.  The medium to send the message is defined by subclass implementations.
    """
    pass

    @abstractmethod
    def sees(self, actor: Actor):
        """Indicates to an actor that the vehicle knows the actor is present.
           Like making eye contact.
           For light communicators, it may be steady lights with a non-descriptive color.
           """
        pass

    def no_longer_sees(self, actor_id: str):
        """The actor is out of range or interest to the vehicle and will no longer have any communication."""
        pass

    def clear(self):
        """Clears all communicators being tracked """
        pass
