import board
import datetime
import RPi.GPIO as GPIO
import json
import neopixel
import os
import requests
import time
from threading import Thread


BASE_URL = "http://<server ip>:3000"
POLLING_DELAY = 1
# Update the ID depending on which client the code is being deployed on
ID = 'amanda'
# id = 'markus'
LAMP_ON_KEY = "lamp_on"
COLOR_KEY = 'color'

def check_server_lamp(request_session) -> bool:
    """
    Gets the status of the lamp from the server

    @param  request_session     Session to persist the connection between requests
    """
    api_url = BASE_URL + "/lamp"
    print(api_url)
    param = {'id': ID}
    response = request_session.get(api_url, params = param, timeout = 5)
    lamp_status = response.json()
    return lamp_status

def send_lamp_off():
    """
    Sets the lamp status on the server to off
    """
    api_url = BASE_URL + "/lamp/off"
    response = requests.post(api_url, timeout = 5)
    response.close()

def send_lamp_on():
    """
    Sets the lamp status on the server to on
    """
    api_url = BASE_URL + "/lamp/on"
    response = requests.post(api_url, timeout = 5)
    response.close()

def turn_on_lamp(pixels, color):
    """
    Turns the physical lamp on on the client side
    """
    pixels.fill(color)
    pixels.show()

def turn_off_lamp(pixels):
    """
    Turns the physical lamp off on the client side
    """
    pixels.fill((0,0,0))
    pixels.show()

class FriendshipLamp:
    """
    Manages a friendship lamp and keeps it synced with the server.
    """
    _lamp_on = False

    # set the LEDs used in the lamp
    _pixels = neopixel.NeoPixel(board.D18, 8, brightness = 0.15)

    # setup the GPIO pins
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __enter__(self):
        """
        Setup a thread when a context manager is used with this class. The thread will
        continuously check for updates from the server.
        """
        __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, 'config.json'), 'r') as f:
            data = json.load(f)
        color = data[COLOR_KEY]
        self._color = tuple(map(int, color.split(',')))
        self._server_thread = Thread(target = self.check_server)
        self._server_thread.daemon = True
        self._server_thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Join the thread when the context manager exits
        """
        # TODO: does this work how I think it does?
        self._server_thread.join()
        pass

    def set_color(self, hex):
        """
        Set the color of the lamp

        @param  hex     hex code for the color
        """
        c = hex.strip('#')
        newColor = tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
        if newColor != self._color:
            self._color = newColor
            if self._lamp_on:
                turn_on_lamp(self._pixels, self._color)
        
            

    def check_server(self):
        """
        Continuously check the server for any updates to the status of the lamp that need to be
        applied to the physical lamp on the client side
        """
        # use a requests session to persist the connection instead of creating
        # a new one for every request
        with requests.Session() as session:
            while True:
                try:
                    server_lamp_status = check_server_lamp(session)
                    server_lamp_on = server_lamp_status[LAMP_ON_KEY]
                    self.set_color(server_lamp_status[COLOR_KEY])
                    print('server says: ' + str(server_lamp_on))
                    if server_lamp_on != self._lamp_on:
                        self._lamp_on = server_lamp_on
                        if self._lamp_on:
                            turn_on_lamp(self._pixels, self._color)
                        elif not self._lamp_on:
                            turn_off_lamp(self._pixels)
                    
                    time.sleep(POLLING_DELAY)
                except Exception as e:
                    time.sleep(POLLING_DELAY)
                    print('error getting server lamp status')
                    print(e)

    def run(self):
        """
        Runs the lamp to manage the light on/off and color. Also responds user
        interactions with the lamp for turning it on.

        The lamps use a touch sensor, which is they the the logic is different from a standard button.
        """
        while True:
            try:
                if GPIO.input(21) == True:
                    if self._lamp_on:
                        turn_off_lamp(self._pixels)
                        self._lamp_on = False
                        send_lamp_off()
                    elif not self._lamp_on:
                        turn_on_lamp(self._pixels, self._color)
                        self._lamp_on = True
                        send_lamp_on()
                    # sleep so the lamp doesn't flicker back and forth while the touch
                    # sensor touched for more than a split second
                    time.sleep(0.5)
            except Exception as e:
                print('error on button press')
                print(e)
                time.sleep(0.5)

if __name__ == '__main__':
    with FriendshipLamp() as lamp:
        lamp.run()