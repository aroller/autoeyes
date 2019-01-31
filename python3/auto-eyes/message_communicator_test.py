import unittest

from actor import Actor
from communicator_test import CommunicatorTest
from message_communicator import MessageCommunicator


class PrintCommunicatorTest(CommunicatorTest, unittest.TestCase):

    @property
    def communicator(self):
        return MessageCommunicator()

    def test_acknowledge_existence_contains_properties(self):
        actor = Actor(actor_id="abc", bearing=234)
        message = self.communicator.acknowledge_existence(actor)
        self.assertRegex(message, actor.actor_id)
        self.assertRegex(message, str(actor.bearing))


if __name__ == '__main__':
    unittest.main()
