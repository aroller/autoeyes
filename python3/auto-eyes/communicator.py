from abc import ABCMeta, abstractmethod

from target import Target


class Communicator(metaclass=ABCMeta):
    """
    Sends messages from the Vehicle to Actors.  The medium to send the message is defined by subclass implementations.
    """
    pass

    @abstractmethod
    def acknowledge_existence(self,target:Target):
        """Inicates to an actor that the vehicle knows the actor is present.
           Like making eye contact.
           For light communicators, it may be steady lights with a non-descriptive color.
           """
        pass

