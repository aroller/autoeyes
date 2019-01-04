import unittest

from communicator_test import CommunicatorTest
from print_communicator import PrintCommunicator


class PrintCommunicatorTest(CommunicatorTest, unittest.TestCase):

    @property
    def communicator(self):
        return PrintCommunicator()


if __name__ == '__main__':
    unittest.main()
