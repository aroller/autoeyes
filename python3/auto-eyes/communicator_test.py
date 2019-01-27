import math
import unittest

from actor import Actor
from abc import ABCMeta, abstractmethod


class CommunicatorTest(metaclass=ABCMeta):

    def test_acknowledge_existence(self):
        actor = Actor(actor_id='a', _bearing=math.pi)
        self.communicator.acknowledge_existence(actor=actor)

    @property
    @abstractmethod
    def communicator(self):
        pass
