from abc import ABCMeta, abstractmethod

from actor import Actor


class Communicator(metaclass=ABCMeta):
    """
    Sends messages from the Vehicle to Actors.  The medium to send the message is defined by subclass implementations.
    """
    pass

    @abstractmethod
    def acknowledge_existence(self,actor:Actor):
        """Indicates to an actor that the vehicle knows the actor is present.
           Like making eye contact.
           For light communicators, it may be steady lights with a non-descriptive color.
           """
        pass


