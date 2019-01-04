import math
import unittest

from actor import Actor
from communicator import Communicator
from target import Target
from abc import ABCMeta, abstractmethod


class CommunicatorTest(metaclass=ABCMeta):

    def test_acknowledge_existence(self):
        target = Target(actor=Actor('a'), bearing=math.pi)
        self.communicator.acknowledge_existence(target=target)

    @property
    @abstractmethod
    def communicator(self):
        pass
