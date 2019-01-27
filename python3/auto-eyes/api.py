#!/usr/bin/env python3

import connexion
from actor import Actor
from vehicle import Vehicle
from pydoc import locate


# Note: All parameters are in the open api naming conventions, not python, to encourage a language independent API.
def put_actor(actorId: str, bearing: float) -> str:
    vehicle.sees(Actor(actorId, bearing))
    return '{actorId} is at {bearing}.'.format(actorId=actorId, bearing=bearing)


def get_actor(actorId: str):
    actors = vehicle.actors()
    if actorId in actors:
        return actors.get(actorId).__dict__
    else:
        return 'Actor with id {actor_id} not found.'.format(actor_id=actorId), 404


def delete_actor(actorId: str) -> bool:
    return vehicle.no_longer_sees(actorId)


def list_actors():
    actors = []
    for actor in vehicle.actors().values():
        actors.append(actor.__dict__)
    return actors


def vehicle_loaded(led_mode) -> Vehicle:
    if led_mode:
        # LED libraries only run on linux, not Mac so dynamically load
        communicator_class_name = 'led_communicator.LedCommunicator'
    else:
        communicator_class_name = 'print_communicator.PrintCommunicator'

    communicator = locate(communicator_class_name)()
    return Vehicle(communicator)


def main():
    app = connexion.FlaskApp(__name__, port=9090, specification_dir='openapi/')
    app.add_api('api.yaml', arguments={'title': 'Autoculi'})
    app.run()


if __name__ == '__main__':
    main()

# TODO: change this global variable into a thread safe persistent resource
vehicle = vehicle_loaded(False)
