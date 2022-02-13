import board
import datetime
import RPi.GPIO as GPIO
import json
import neopixel
import os
import requests
import time
from threading import Thread

# import logging
# logging.basicConfig(level=logging.DEBUG, format="%(message)s")

BASE_URL = "https://lamp-lamp.herokuapp.com"
POLLING_DELAY = 1
id = 'amanda'
# id = 'markus'
LAMP_ON_KEY = "lamp_on"
COLOR_KEY = 'color'


def check_server_lamp(request_session) -> bool:
    api_url = BASE_URL + "/lamp"
    print(api_url)
    param = {'id': id}
    response = request_session.get(api_url, params = param, timeout = 5)
    # print(response.json())
    # print(response.status_code)
    lamp_status = response.json()
    temp = response.content
    return lamp_status

def send_lamp_off():
    api_url = BASE_URL + "/lamp/off"
    response = requests.post(api_url, timeout = 5)
    response.close()
    # print(response.json())
    # print(response.status_code)

def send_lamp_on():
    api_url = BASE_URL + "/lamp/on"
    response = requests.post(api_url, timeout = 5)
    response.close()
    # print(response.json())
    # print(response.status_code)

def turn_on_lamp(pixels, color):
    pixels.fill(color)
    # pixels.fill((255,255,255))
    pixels.show()

def turn_off_lamp(pixels):
    pixels.fill((0,0,0))
    pixels.show()

class Lamp:
    # if the lamp is currently on
    _lamp_on = False
    # sync with server if the time is later this time
    _check_server_after = datetime.datetime.now()
    # tells us if we are currently checking the server
    _checking_server = False

    _pixels = neopixel.NeoPixel(board.D18, 8, brightness = 0.15)

    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __enter__(self):
        __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, 'config.json'), 'r') as f:
            data = json.load(f)
        color = data['color']
        self._color = tuple(map(int, color.split(',')))
        self._server_thread = Thread(target = self.check_server)
        self._server_thread.daemon = True
        self._server_thread.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # self._server_thread.join()
        pass

    def check_server(self):
        with requests.Session() as s:
            while True:
                try:
                    # print('check server')
                    # if datetime.datetime.now() < self._check_server_after:
                    #     time.sleep(POLLING_DELAY)
                    #     continue
                    server_lamp_status = check_server_lamp(s)
                    server_lamp_on = server_lamp_status[LAMP_ON_KEY]
                    self._color = server_lamp_status[COLOR_KEY]
                    print('server says: ' + str(server_lamp_on))
                    if server_lamp_on != self._lamp_on:
                        self._lamp_on = server_lamp_on
                        if self._lamp_on:
                            turn_on_lamp(self._pixels, self._color)
                        elif not self._lamp_on:
                            turn_off_lamp(self._pixels)
                    
                    time.sleep(POLLING_DELAY)
                    self._checking_server = False
                except Exception as e:
                    time.sleep(POLLING_DELAY)
                    self._checking_server = False
                    print('error getting server lamp status')
                    print(e)

    def run(self):
        while True:
            try:
                if GPIO.input(21) == True:
                    if self._lamp_on:
                        send_lamp_off()
                        self._lamp_on = False
                        turn_off_lamp(self._pixels)
                        # self._check_server_after = datetime.datetime.now() + datetime.timedelta(hours = 1)
                    elif not self._lamp_on:
                        send_lamp_on()
                        self._lamp_on = True
                        turn_on_lamp(self._pixels, self._color)
                        # self._check_server_after = datetime.datetime.now()
                    time.sleep(0.5)
            except Exception as e:
                print('error on button press')
                print(e)

if __name__ == '__main__':
    with Lamp() as lamp:
        lamp.run()