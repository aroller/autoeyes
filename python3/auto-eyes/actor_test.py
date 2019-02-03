import unittest
from actor import Actor, Direction


class ActorTest(unittest.TestCase):

    def test_actor_id_assigned_during_construction(self):
        id = "test"
        bearing = 170.1
        actor = Actor(id, bearing)
        self.assertEqual(id, actor.actor_id);
        self.assertEqual(bearing, actor.bearing);

    def test_right_value_builds_right_enum(self):
        self.assertEqual("right", Direction.RIGHT.value)
        self.assertEqual(Direction.RIGHT, Direction(Direction.RIGHT.value))

    def test_left_value_builds_left_enum(self):
        self.assertEqual("left", Direction.LEFT.value)
        self.assertEqual(Direction.LEFT, Direction(Direction.LEFT.value))


if __name__ == '__main__':
    unittest.main()
