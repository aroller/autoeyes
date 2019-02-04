import unittest

from overrides import overrides

from actor import Actor
from communicator_test import CommunicatorTest
from message_communicator import MessageCommunicator


class MessageCommunicatorTest(CommunicatorTest, unittest.TestCase):

    def __init__(self, method_name: str):
        super().__init__(method_name)

    @property
    @overrides
    def communicator(self):
        return MessageCommunicator()

    def test_acknowledge_existence_contains_properties(self):
        actor = Actor(actor_id="abc", bearing=234)
        message = self.communicator.sees(actor)
        self.assertRegex(message, actor.actor_id)
        self.assertRegex(message, str(actor.bearing))


if __name__ == '__main__':
    unittest.main()
