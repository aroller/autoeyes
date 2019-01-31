#!/usr/bin/env python3
from http import HTTPStatus
import connexion
from flask_cors import CORS

from actor import Actor
from api_model import ApiModel, ApiModelSerializer
from led_communicator import LedCommunicator
from led_strip_controller import LedStripController
from message_communicator import MessageCommunicator
from vehicle import Vehicle
from pydoc import locate


# Note: All parameters are in the open api naming conventions, not python, to encourage a language independent API.
def put_actor(actorId: str, bearing: float):
    actor = vehicle.sees(Actor(actorId, bearing))
    if actor:
        return actor.api_json()
    else:
        return None, HTTPStatus.NO_CONTENT


def get_actor(actorId: str):
    actors = vehicle.actors
    if actorId in actors:
        return actors[actorId].api_json()
    else:
        return 'Actor with id {actor_id} not found.'.format(actor_id=actorId), HTTPStatus.NOT_FOUND


def delete_actor(actorId: str) -> bool:
    return vehicle.no_longer_sees(actorId)


def list_actors():
    return ApiModelSerializer.to_json(vehicle.actors.values())


def list_communicators():
    return ApiModelSerializer.to_json(vehicle.communicators)


def vehicle_loaded(led_mode) -> Vehicle:
    pixel_count = 300
    if led_mode:
        # LED libraries only run on linux, not Mac so dynamically load
        controller_class_name = 'rpi_ws281x_led_strip.RpiWs281xLedStripController'
        controller = locate(controller_class_name)(pixel_count)

    else:
        controller = LedStripController(pixel_count)

    return Vehicle([LedCommunicator(controller), MessageCommunicator()])


def main():
    app = connexion.FlaskApp(__name__, port=9090, specification_dir='openapi/')
    app.add_api('api.yaml', arguments={'title': 'Autoculi'})
    CORS(app.app)
    app.run()


if __name__ == '__main__':
    main()

# TODO: change this global variable into a thread safe persistent resource
vehicle = vehicle_loaded(False)
