import unittest
from actor import Actor


class ActorTest(unittest.TestCase):

    def test_actor_id_assigned_during_construction(self):
        id = "test"
        bearing = 170.1
        actor = Actor(id, bearing)
        self.assertEqual(id, actor.actor_id);
        self.assertEqual(bearing, actor.bearing);

if __name__ == '__main__':
    unittest.main()
