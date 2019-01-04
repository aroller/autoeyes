import unittest
from actor import Actor


class ActorTest(unittest.TestCase):

    def test_actor_id_assigned_during_construction(self):
        id = "test"
        self.assertEqual(id, Actor(id).actor_id);

if __name__ == '__main__':
    unittest.main()
