"""
from hydroponics.config import load_config, load_url_config, print_config
cf = load_config()
cw = load_url_config()
print(cw["version"])
"""
import time, os, ubinascii
import urequests, json
from util.led import blink
from util.wifi_connect import read_wifi_config, WiFiConnect

from util.octopus import get_eui, w

deviceID = str(get_eui())

place = "none"      # group of IoT > load from config/garden.json
minute = 10         # 1/10 for data send
last8dID = True     # for db only 8 bytes device ID
wifi_retries = 100  # for wifi connecting

# hard-code config / daefault
timeInterval = 10
tempoffset = 0      # hard correction of err/wrong dallas
startLight = 12
stopLight = 12
cloudConfig = False
cloudUpdate = False
cloudConfigDynamic = True
lightIntensity = 1023

oldLightIntensity = 1023

# Defaults - sensors
isTemp = 0          # temperature
isLight = 0         # light (lux)
isMois = 0          # moisture
isAD = 0            # AD input voltage
isADL = 0           # AD photoresistor
isADT = 0           # AD thermistor   
isPH = 0            # TODO  
isPressure = 0      # 
prewLight = False
prewRelay = False
pumpStat = 0
confVer = 0         # config version 0.3>1

runDemo = False
pumpDurat = 0
confUID = 0

# config data structure
conf_data={
"config version": "version",
"place": "place",
"timeInterval minutes: ": "timeinterval",
"start light": "startlight",
"stop light": "stoplight",
"pump time nodes": "pumpnodes",
"pump duration": "pumpduration"
}

config = {}

def load_config(configFile = 'config/garden.json'):
    print("load "+configFile+" >")
    iot_config = {}  # main system config - default/flash-json/web-cloud
    try:
        with open(configFile, 'r') as f:
            d = f.read()
            f.close()
            iot_config = json.loads(d)
    except:
        print("Err. or " + configFile + " does not exist")
    return iot_config


def load_url_config():
    url_config = {}
    urlApi ="http://www.octopusengine.org/api/hydrop/"
    urlConf = urlApi + "/config/" + deviceID + ".json"
    print("--- load URL Config >")
    try:
        response = urequests.get(urlConf)
        url_config = json.loads(response.text)
        print(str(url_config))
    except:
        print("Err.loadCloudConfig() - connect? json exist?")
    return url_config


def change_config(): # once / no save
    global confVer, place, timeInterval, runDemo, startLight, stopLight, lightIntensity, pumpDurat, pumpNodes
    print("--- change Config() >")
    try:
        if(url_config.get('startlight') != None):
            startLight = url_config.get('startlight')
            stopLight = url_config.get('stoplight')
            lightIntensity = url_config.get('lightintensity')
            pumpDurat = url_config.get('pumpduration')
        else:
            print("Off-line -> url_config.Null")    
        # pumpNodes = url_config.get('pumpnodes')
    except:
        print("Err.changeConfig() - bad json?")


def print_config(cc):
    print()
    print('=' * 33)
    for ix in conf_data.values():
        try:
            # print(ix, cc[ix])
            print(" %15s - %s " % (ix, cc[ix] ))
        except:
            Err_print_config = True
    print('=' * 33)

"""
def print_config-old():

    if Debug:
        print()
        print('=' * 33)
        print("config version: " + str(confVer))
        print("place: " + place)
        print("timeInterval minutes: " + str(timeInterval))
        print('-' * 12)
        print("start light - hour: " + str(startLight))
        print("stop light - hour: " + str(stopLight))
        print("light intensity: " + str(lightIntensity))
        print("pump hour nodes: " + str(pumpNodes))
        print("pump minute duration: " + str(pumpDurat))
        print('=' * 12)
        print("run demo / test: " + str(runDemo))
        print("cloudConfig: " + str(cloudConfig))
        print("cloudUpdate: " + str(cloudUpdate))        
        print('=' * 33)
        print("setup vector [ Temp Light Moist Analog AL AT DallasOffset ]:")
        print(str(isTemp)+str(isLight)+str(isMois)+str(isAD)+str(isADL)+str(isADT)+str(tempoffset))        
        print()  


def loadConfig-old():
    global confVer, place, timeInterval, runDemo, startLight, stopLight, lightIntensity, pumpDurat, pumpNodes
    global confUID, Debug, last8dID, isTemp, isLight, isMois, isAD, isADL, isADT, cloudConfig, cloudUpdate, tempoffset
    
    configFile = 'config/garden.json'
    if Debug: print("load "+configFile+" >")
    try:
        with open(configFile, 'r') as f:
            d = f.read()
            f.close()
            iot_config = json.loads(d)

        confVer = iot_config.get('version')
        place = iot_config.get('place')
        confUID = iot_config.get('uid')
        timeInterval = iot_config.get('timeinterval')
        runDemo = iot_config.get('rundemo')
        startLight = iot_config.get('startlight')
        stopLight = iot_config.get('stoplight')
        lightIntensity = iot_config.get('lightintensity')
        pumpDurat = iot_config.get('pumpduration')
        pumpNodes = iot_config.get('pumpnodes')
        Debug = iot_config.get('debug')
        last8dID = iot_config.get('uid8')

        isTemp = iot_config.get('mtemp') # m=measure temperature
        isLight = iot_config.get('mlight')
        isMois = iot_config.get('mmoist')
        isAD = iot_config.get('manalog')
        isADL = iot_config.get('manlight')
        isADT = iot_config.get('mantemp')

        tempoffset = int(iot_config.get('tempoffset'))

        cloudConfig = iot_config.get('cloudconfig')
        cloudUpdate = iot_config.get('cloudupdate')

    except:
        print("Err. or 'config/garden.json' does not exist")

"""

# ----------------------- init > config ----------------------

#loadConfig()
#printConfig()

#rint(str(isTemp)+str(isLight)+str(isMois)+"/"+str(isAD)+str(isADL)+str(isADT)+str(tempoffset))  

# timeSetup()
# logDevice()

