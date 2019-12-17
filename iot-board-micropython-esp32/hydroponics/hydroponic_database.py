"""
http request
mqtt
influx
...
ampy -p /COM6 put ./hydroponics/send_data.py hydroponics/send_data.py
ampy -p /COM6 put ./config/garden.json config/garden.json
from hydroponics.send_data import send_data_get, send_data_post
"""

from time import sleep, sleep_ms
import urequests
from util.octopus import Env
from util.database import Database


class HydroponicsDatabase(Database):
    def __init__(self, config):
        self.__urlPOST = config.get("urlpost") # "http://www.yourweb.org/iot18/add18.php"
        self.__place = config.get("place")
        self.__deviceID = Env.uID


    def __send_form_data(self, val_type, val): # POST >
        header = {}
        header["Content-Type"] = "application/x-www-form-urlencoded"
        try:
            postdata = "device={0}&place={1}&value={2}&type={3}".format(self.__deviceID, self.__place, val, val_type)
            print(postdata)
            res = urequests.post(self.__urlPOST, data=postdata, headers=header)
            res.close()
            print("send_form_data_post.OK")
        except Exception as e:
            print("Exception: {0}".format(e))
            print("Err.send_form_data_post")

    def log_device(self, ver):
        logVer =  int(float(ver)*100)
        self.write(log_ver = logVer)

    def write(self, *args, **kwargs):
        for k, v in kwargs.items():
            self.__send_form_data(k, v)
