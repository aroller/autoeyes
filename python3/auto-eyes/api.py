#!/usr/bin/env python3

import connexion
from actor import Actor
from vehicle import Vehicle

vehicle = Vehicle()


# Note: All parameters are in the open api naming conventions, not python, to encourage a language independent API.

def put_actor(actorId: str, bearing: float) -> str:
    vehicle.sees(Actor(actorId, bearing))
    return '{actorId} is at {bearing}.'.format(actorId=actorId, bearing=bearing)


def get_actor(actorId: str) -> str:
    return '{actor_id} found: {found}'.format(actor_id = actorId,found = actorId in vehicle.actors());

def delete_actor(actorId: str) -> str:
    return vehicle.no_longer_sees(actorId)

def get_actors() -> str:
    return "{count} actors found".format(count=len(vehicle.actors()))


if __name__ == '__main__':
    app = connexion.FlaskApp(__name__, port=9090, specification_dir='openapi/')
    app.add_api('api.yaml', arguments={'title': 'Autoculi'})
    app.run()
