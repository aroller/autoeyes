#!/usr/bin/env python3
import atexit
import os
import threading
from http import HTTPStatus
from pydoc import locate
from subprocess import call
from time import time, sleep

import connexion
from flask_cors import CORS

from actor import Actor, Action, Direction, Urgency
from api_model import ApiModelSerializer
from led_communicator import LedCommunicator
from led_strip_controller import LedStripController
from message_communicator import MessageCommunicator
from vehicle import Vehicle

# change this number to match the number of led pixels on your strip
PIXEL_COUNT = 207
# change to true if running on a Raspberry PI with the WS2812b library installed and LED strip connected
LED_MODE = 'AV_EYES_LED_MODE' in os.environ

# Background processor to handle flashing and other animations for urgency, direction, etc.
animator_thread = threading.Thread()
ANIMATOR_CALLS_PER_SECOND = 1


# Note: All parameters are in the open api naming conventions, not python, to encourage a language independent API.
def put_actor(actorId: str,
              bearing: float,
              action: str = None,
              direction: str = None,
              urgency: str = None):
    if action is not None:
        action = Action(action)
    if direction is not None:
        direction = Direction(direction)
    if urgency is not None:
        urgency = Urgency(urgency)

    actor = vehicle.sees(Actor(actor_id=actorId,
                               bearing=bearing,
                               action=action,
                               direction=direction,
                               urgency=urgency))
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


def delete_actor(actorId: str):
    if vehicle.no_longer_sees(actorId):
        return True
    else:
        return "Actor '{actor_id}' is not found.".format(actor_id=actorId), 404


def list_actors():
    return ApiModelSerializer.to_json(vehicle.actors.values())


def list_communicators():
    return ApiModelSerializer.to_json(vehicle.communicators)


def system_shutdown():
    """Shuts down the raspberry pi gracefully.  Yes, probably a bad idea and something better provided
        from a physical switch.
    """
    vehicle.clear()
    print("********* Shut Down command given *********")
    call("sudo shutdown -h now", shell=True)


def vehicle_loaded(led_mode) -> Vehicle:
    if led_mode:
        # LED libraries only run on linux, not Mac so dynamically load
        controller_class_name = 'rpi_ws281x_led_strip_controller.RpiWs281xLedStripController'
        controller = locate(controller_class_name)(PIXEL_COUNT)
        print("loading {controller}".format(controller=controller_class_name))
    else:
        print("using default LED Strip Controller")
        controller = LedStripController(PIXEL_COUNT)

    led_communicator = LedCommunicator(controller)
    led_communicator.welcome_light_show()
    return Vehicle([led_communicator])


def animator_thread_interrupt():
    global animator_thread
    animator_thread.cancel()


def animator_call():
    time_last_printed = 0
    times_called = 0
    sleep_time = 1 / ANIMATOR_CALLS_PER_SECOND

    # simple loop is chosen over multiple threading for simplicity at the cost of exact calls
    # each animator should return as quick as possible and manage time on their own making no calls per time assumptions
    # Threading.Timer can be used if individual threads would be better https://stackoverflow.com/questions/14384739/
    while True:
        times_called = times_called + 1

        current_seconds = int(time())
        if current_seconds != time_last_printed:
            print("animator called {times} times at {seconds}".format(times=times_called, seconds=current_seconds))
            time_last_printed = current_seconds
        sleep(sleep_time)


def animator_thread_start():
    # Do initialisation stuff here
    global animator_thread
    # Create your thread
    print("starting thread")
    animator_thread = threading.Thread(target=animator_call)
    animator_thread.start()


def main():
    app = connexion.FlaskApp(__name__, port=9090, specification_dir='openapi/')
    app.add_api('api.yaml', arguments={'title': 'Autoculi'})
    CORS(app.app)
    # animator_thread_start()
    # atexit.register(animator_thread_interrupt)
    app.run()


if __name__ == '__main__':
    main()

# TODO: change this global variable into a thread safe persistent resource
vehicle = vehicle_loaded(LED_MODE)
