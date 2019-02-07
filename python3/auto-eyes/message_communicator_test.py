import unittest

from overrides import overrides

from actor import Actor
from message_communicator import MessageCommunicator


class PrintCommunicatorTest( unittest.TestCase):

    @property
    def communicator(self):
        return MessageCommunicator()

    def test_acknowledge_existence_contains_properties(self):
        actor = Actor(actor_id="abc", bearing=234)
        message = self.communicator.sees(actor)
        self.assertRegex(message, actor.actor_id)
        self.assertRegex(message, str(actor.bearing))


if __name__ == '__main__':
    unittest.main()
