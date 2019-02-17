#!/usr/bin/env python3
import atexit
import os
import threading
from http import HTTPStatus
from pydoc import locate
from subprocess import call
from time import time, sleep

import connexion
import requests
from flask import send_from_directory
from flask_cors import CORS

from actor import Actor, Action, Direction, Urgency
from api_model import ApiModelSerializer
from led_communicator import LedCommunicator
from led_strip_controller import LedStripController
from vehicle import Vehicle

# change this number to match the number of led pixels on your strip
PIXEL_COUNT = 207
# change to true if running on a Raspberry PI with the WS2812b library installed and LED strip connected
LED_MODE = 'AV_EYES_LED_MODE' in os.environ

# Background processor to handle flashing and other animations for urgency, direction, etc.
animator_thread = None
seconds_between_animation = None
animator_lock = threading.Lock()


# Note: All parameters are in the open api naming conventions, not python, to encourage a language independent API.
def put_actor(actorId: str,
              bearing: float,
              action: str = None,
              direction: str = None,
              urgency: str = None,
              timeSeen: str = None):
    """Sets the state of the actor and updates the list in the vehicle."""
    if action is not None:
        action = Action(action)
    if direction is not None:
        direction = Direction(direction)
    if urgency is not None:
        urgency = Urgency(urgency)

    try:
        actor = vehicle.sees(Actor(actor_id=actorId,
                                   bearing=bearing,
                                   action=action,
                                   direction=direction,
                                   urgency=urgency,
                                   time_seen=timeSeen))
    except ValueError as e:
        return str(e), HTTPStatus.CONFLICT
    # actor is modified so there may be a need for animation
    animate()

    if actor:
        return actor.api_json()
    else:
        return None, HTTPStatus.NO_CONTENT


def get_actor(actorId: str):
    """Shows the state of any actor, if it exists."""
    actors = vehicle.actors
    if actorId in actors:
        return actors[actorId].api_json()
    else:
        return 'Actor with id {actor_id} not found.'.format(actor_id=actorId), HTTPStatus.NOT_FOUND


def delete_actor(actorId: str):
    """Removes the actor from the sight of vehicle. """
    if vehicle.no_longer_sees(actorId):
        return HTTPStatus.NO_CONTENT
    else:
        return "Actor '{actor_id}' is not found.".format(actor_id=actorId), HTTPStatus.NOT_FOUND


def list_actors():
    """"Provides all actors the vehicle currently sees."""
    return ApiModelSerializer.to_json(vehicle.actors.values())


def client_file(path):
    """Serves up static html files and supporting resources like js, images, etc."""
    return send_from_directory('client', path)


def system_shutdown():
    """Shuts down the raspberry pi gracefully.  Yes, probably a bad idea and something better provided
        from a physical switch.
    """
    vehicle.sees(Actor('shutdown', 0))
    sleep(1)
    vehicle.clear()
    print("********* Shut Down command given *********")
    call("sudo shutdown -h now", shell=True)


def vehicle_loaded(led_mode: bool) -> Vehicle:
    """Creates the vehicle with the communicators loaded.  Based on the parameter, the led controller will
    load with the raspberry pi ws281x controller. This is necessary since the raspberry pi code will cause
    all executions to fail when testing on dev environments."""
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
    """Stops the current thread, if any, when the program is stopped"""
    global animator_thread
    if animator_thread is not None:
        animator_thread.cancel()


def animator_call():
    """Simply makes a local REST call to animate and queues up a repeat call using a timer thread"""
    #  https://stackoverflow.com/questions/14384739/
    global animator_thread
    global seconds_between_animation
    if seconds_between_animation is not None:
        requests.put('http://localhost:9090/v1.0/animations')  # --> animate()
        animator_thread = threading.Timer(seconds_between_animation / 2, animator_call)
        animator_thread.start()


def animate():
    """refreshes the scene to reflect all actors and to toggle pixels based on their urgency or direction.
        FIXME: This should be at the LED Communicator level and not require http calls
    """
    global seconds_between_animation
    global animator_thread
    with animator_lock:
        seconds_between_animation = vehicle.animate(time())
        if seconds_between_animation is not None:
            if animator_thread is None:
                # avoids starting multiple timer threads
                animator_thread = threading.Timer(seconds_between_animation, animator_call)
                animator_thread.start()
        else:
            if animator_thread is not None:
                # no thread indicates one can start again in the future
                animator_thread = None


def main():
    app = connexion.FlaskApp(__name__,
                             port=9090,
                             specification_dir='openapi/')
    app.add_api('api.yaml', arguments={'title': 'Auto Eyes'})
    CORS(app.app)
    atexit.register(animator_thread_interrupt)
    app.run()


if __name__ == '__main__':
    main()

# TODO: change this global variable into a thread safe persistent resource
vehicle = vehicle_loaded(LED_MODE)
