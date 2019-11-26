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

class SendData():
    pass

class SendHydroponicsData(SendData):
    def __init__(self, config):
        self.urlPOST = config.config.get("urlpost") # "http://www.yourweb.org/iot18/add18.php"
        self.place = config.config.get("place")
        self.deviceID = Env.uID

    """
        OLD: DO NOT USE GET to send data, NEVER EVER!
        def send_data_get(self, val_type="log_ver", val=0): # GET >
            try:
                url = urlGET + "?device=" + str(deviceID) + "&type=" + val_type + "&value=" + str(val)
                print(url)
                req = urequests.get(url)
                return("send_data_get.OK")
            except Exception as e:
                print("Exception: {0}".format(e))
                return("Err.send_data_get")
    """

    def send_form_data(self, val_type, val): # POST >
        header = {}
        header["Content-Type"] = "application/x-www-form-urlencoded"
        try:
            postdata = "device={0}&place={1}&value={2}&type={3}".format(self.deviceID, self.place, val, val_type)
            print(postdata)
            res = urequests.post(self.urlPOST, data=postdata, headers=header)
            return("send_form_data_post.OK")
        except Exception as e:
            print("Exception: {0}".format(e))
            return("Err.send_form_data_post")


    def log_device(self, ver):
        logVer =  int(float(ver)*100)
        self.send_form_data_post("log_ver", logVer)

    """
    # -----------------------
    # Influx db
    influxWriteURL = ""
    influxWriteURL = iot_config.get('influxWriteURL')

    def influxSend():
            try:
            influx_tags   = dict()
            influx_fields = dict()

            influx_tags["device"] = deviceID
            influx_tags["place"]  = place

            # GET >
            #urlGET = urlGet + "?device=" + deviceID + "&type=temp1&value=" + str(tw)
            #req = urequests.post(url)
            if isTemp:
                ds.convert_temp()
                time.sleep_ms(750)
                for t in ts:
                    temp = ds.read_temp(t)
                    influx_fields["temp"] = temp
                    tw = int(temp*10)
                    postdata_t = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, str(tw),"t{0}".format(bytearrayToHexString(t)[-6:]))
                    res = urequests.post(urlPOST, data=postdata_t, headers=header)
                    time.sleep_ms(1000)

            if isLight:
                if bhLight:
                    numlux = sbh.luminance(BH1750.ONCE_HIRES_1)
                    influx_fields["light1"] = numlux
                    postdata_l = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, str(int(numlux)),"ligh1")
                    res = urequests.post(urlPOST, data=postdata_l, headers=header)
                    time.sleep_ms(1000)

                if bh2Light:
                    numlux = sbh2.luminance(BH1750.ONCE_HIRES_1)
                    influx_fields["light2"] = numlux
                    postdata_l = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, str(int(numlux)),"ligh2")
                    res = urequests.post(urlPOST, data=postdata_l, headers=header)
                    time.sleep_ms(1000)

                if tslLight:
                    numlux = tsl.read()
                    influx_fields["light3"] = numlux
                    postdata_l = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, str(int(numlux)),"ligh3")
                    res = urequests.post(urlPOST, data=postdata_l, headers=header)
                    time.sleep_ms(1000)

            if isMois:
                sM = get_moisture()
                if   isOLED:
                    valmap = map(sM, 0, 4050, 0, 126)
                    displBarSlimH(oled, valmap, 11)
                influx_fields["mois1"] = sM
                postdata_l = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, str(int(sM)),"mois1")
                res = urequests.post(urlPOST, data=postdata_l, headers=header)

            if isAD:
            adV = getADvolt(Debug)
            displMessage("AD:"+str(adV),2) #only test
            influx_fields["adraw"] = adV
            postdata_l = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, str(int(adV)),"adraw")
            res = urequests.post(urlPOST, data=postdata_l, headers=header)

            postdata_tags   = ','.join(["%s=%s" % (k, v) for (k, v) in influx_tags.items()])
            postdata_fields = ','.join(["%s=%s" % (k, v) for (k, v) in influx_fields.items()])

            postdata_influx = "hydrobox,{0} {1}".format(postdata_tags, postdata_fields)
            res = urequests.post(influxWriteURL, data=postdata_influx)

        except:
            displMessage("Err: send data",3) 

    """