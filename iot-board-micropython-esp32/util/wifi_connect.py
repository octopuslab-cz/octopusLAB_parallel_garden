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
        self.events_timeout = []
        self.retries = retries

    def __call_events_connecting__(self, retry):
        for f in self.events_connecting:
            f(retry)

    def __call_events_connected__(self, sta):
        for f in self.events_connected:
            f(sta)

    def __call_events_timeout__(self):
        for f in self.events_timeout:
            f()

    def events_add_connecting(self, func):
        self.events_connecting.append(func)

    def events_add_connected(self, func):
        self.events_connected.append(func)

    def events_add_timeout(self, func):
        self.events_timeout.append(func)

    def connect(self, ssid, password):
        retry = 1
        # get an instance of the sta_if WiFi interface
        sta_if = network.WLAN(network.STA_IF)
        
        # check if we are already connected to a WiFi
        if sta_if.isconnected():
            self.__call_events_connected__(sta_if)
            return True

        # activate interface
        sta_if.active(True)

        # connect to network via provided ID
        sta_if.connect(ssid, password)

        while not sta_if.isconnected():
            if retry == self.retries:
                break

            self.__call_events_connecting__(retry)
            retry+=1
            sleep_ms(100)
            

        # print connection info - automatic
        # currently this prints out as if no connection was established - giving 0.0.0.0 sd ip
        # however, connection IS made and functional
        if sta_if.isconnected():
            self.__call_events_connected__(sta_if)
            return True
        else:
            self.__call_events_timeout__()
            sta_if.active(False)
            return False

def read_wifi_config():
    # TODO file does not exist
    f = open('config/wifi.json', 'r')
    d = f.read()
    f.close()
    return json.loads(d)
