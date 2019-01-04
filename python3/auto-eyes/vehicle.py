from actor import Actor
from target import Target


class Vehicle:

    def sees(self, target: Target):
        """To confirm that the vehicle sees the actor at the target."""
        print("Spotted {} at {}.".format(target.actor.actor_id,target.bearing))
