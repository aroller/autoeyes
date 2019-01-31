import unittest

from communicator_test import CommunicatorTest
from led_communicator import LedCommunicator
from message_communicator import MessageCommunicator


class LedCommunicatorTest(CommunicatorTest, unittest.TestCase):

    @property
    def communicator(self):
        return LedCommunicator()

if __name__ == '__main__':
    unittest.main()
