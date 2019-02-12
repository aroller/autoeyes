# Autoculi Python3 Library

Provides the features at a portable level decoupling the 
LED strip that will be used as the display.

see [Project Autoculi](https://autoculi.org);


Run the _print_ unit tests to demonstrate the scenarios 
in any environment to demonstrate results as text in the console:

`python3 print_communicator_test.py`

Run the _led_ unit tests to demonstrate the scenarios on a 
Raspberry PI connected to a WS2812B LED strip (per the [demo setup](/demo)):

`sudo python3 led_communicator_test.py`


# API

A REST API is provided to allow communications with the LED code from any 
source on the network.  

## Flask
[Flask](http://flask.pocoo.org/) is an API language and server 
that provides a Rest Implementation for web services and documentation.

### Flask 
[Flaggser](https://github.com/rochacbruno/flasgger) provides Open API documentation 

## Quart

Quart is the next generation API that works with Flask annotations, 
but provides asynchronous capabilities which may be useful to reduce
network overload of API calls waiting for a process to finish.

The use of Quart is delayed, for simplicity's sake, since it requires python 3.7 which is [not yet 
built for Raspberry PI](https://www.ramoonus.nl/2018/06/30/installing-python-3-7-on-raspberry-pi/) as of 12/15/2019. 

More documentation to come...


Setup Access Point

http://www.raspberryconnect.com/network/item/333-raspberry-pi-hotspot-access-point-dhcpcd-method

