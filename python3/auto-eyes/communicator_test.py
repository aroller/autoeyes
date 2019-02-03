import math
import unittest

from actor import Actor
from abc import ABCMeta, abstractmethod


class CommunicatorTest(unittest.TestCase, metaclass=ABCMeta):

    def test_acknowledge_existence_does_not_fail(self):
        actor = Actor(actor_id='a', bearing=math.pi)
        self.assertIsNotNone(self.communicator,"Your test class must provide the communicator instance")
        self.communicator.sees(actor=actor)

    @property
    @abstractmethod
    def communicator(self):
        pass
