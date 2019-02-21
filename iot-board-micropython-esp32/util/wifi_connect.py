# include this in boot.py or main.py as WiFiConnect

# Usage:
# from WiFiConnect import WiFiConnect
# w = WiFiConnect()
# w.events_add_connecting(function to callback connecting)
# w.events_add_connected(function to callback connected)
# w.connect(ssid, password)

# Includes
import network
import json, ujson  # suspicious?
from time import sleep, sleep_ms

class WiFiConnect:
    def __init__(self, retries = 0):
        self.events_connecting = []
        self.events_connected = []
        self.events_disconnected = []
        self.events_timeout = []
        self.retries = retries
        self.lastState = False

    def __call_events_connecting__(self, retry):
        for f in self.events_connecting:
            f(retry)

    def __call_events_connected__(self, sta):
        for f in self.events_connected:
            f(sta)

    def __call_events_disconnected__(self):
        for f in self.events_disconnected:
            f()

    def __call_events_timeout__(self):
        for f in self.events_timeout:
            f()

    def events_add_connecting(self, func):
        self.events_connecting.append(func)

    def events_add_connected(self, func):
        self.events_connected.append(func)

    def events_add_disconnected(self, func):
        self.events_disconnected.append(func)

    def events_add_timeout(self, func):
        self.events_timeout.append(func)

    def connect(self, ssid, password):
        retry = 1
        # get an instance of the sta_if WiFi interface
        self.sta_if = network.WLAN(network.STA_IF)
        
        # check if we are already connected to a WiFi
        if self.sta_if.isconnected():
            self.__call_events_connected__(self.sta_if)
            return True

        # activate interface
        self.sta_if.active(True)

        # connect to network via provided ID
        self.sta_if.connect(ssid, password)

        while not self.sta_if.isconnected():
            if retry == self.retries:
                break

            self.__call_events_connecting__(retry)
            retry+=1
            sleep_ms(100)
            

        # print connection info - automatic
        # currently this prints out as if no connection was established - giving 0.0.0.0 sd ip
        # however, connection IS made and functional
        self.lastState = self.sta_if.isconnected()

        if self.sta_if.isconnected():
            self.__call_events_connected__(self.sta_if)
            return True
        else:
            self.__call_events_timeout__()
            self.sta_if.active(False)
            return False

    def isconnected(self):
        return self.sta_if.isconnected()

    def handle_wifi(self):
        print("Handle wifi running: last: {0}, now: {1}".format(self.lastState, self.sta_if.isconnected()))
        if self.lastState and not self.sta_if.isconnected():
            print("Handle wifi False")
            self.lastState = False
            self.__call_events_disconnected__()

        if not self.lastState and self.sta_if.isconnected():
            print("Handle wifi True")
            self.lastState = True
            self.__call_events_connected__(self.sta_if)


def read_wifi_config():
    # TODO file does not exist
    f = open('config/wifi.json', 'r')
    d = f.read()
    f.close()
    return json.loads(d)
