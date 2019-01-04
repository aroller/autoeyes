import unittest

from communicator_test import CommunicatorTest
from led_communicator import LedCommunicator
from print_communicator import PrintCommunicator


class PrintCommunicatorTest(CommunicatorTest, unittest.TestCase):

    @property
    def communicator(self):
        return LedCommunicator()

if __name__ == '__main__':
    unittest.main()
