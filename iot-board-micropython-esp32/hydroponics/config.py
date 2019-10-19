"""
from hydroponics.config import load_config, load_url_config, print_config, load_env_setup, print_env_setup
es = load_env_setup()
print_env_setup(es)
print(es["relay"])

cf = load_config() # from file
cw = load_url_config() # from "web"
print(cw["version"]) # print(cw["pumpnodes"][1])
"""

import urequests, json
from util.octopus import get_eui
deviceID = str(get_eui())


# ------------------------------
# setup peripherials / sensors - data structure
conf_setup=[
["built_in_led","led"],
["WS rgb led","ws"],
["i2c light sensor","light"],
["temperature (dall.)","temp"],
["A/D moisture","mois"],
["A/D capacit moist.","cmois"],
["A/D inp.voltage","ad0"],
["A/D photoresist.","ad1"],
["A/D thermistor","ad2"],
["mosFet pwm led","fet"],
["relay","relay"]
]


def get_conf_setup():
    return conf_setup


def load_env_setup():
    from util.io_config import get_from_file as get_io_config_from_file
    # read current settings from json to config object
    io_conf = get_io_config_from_file()
    return io_conf


def print_env_setup(io_conf):
    print()
    print('=' * 39)
    for ix in conf_setup:
        try:
            # print(ix, cc[ix]) # dict{}
            print(" %25s - %s " % (ix[0], io_conf[ix[1]] ))
        except:
            Err_print_config = True
    print('=' * 39)


# config data structure - is not dict, because bad sort
conf_data=[
["config version", "version"],
["place (name)", "place"],
["temperature offset", "tempoffset"],
["start light [hour]", "startlight"],
["stop light [hour]", "stoplight"],
["light intensity (0-1023)", "lightintensity"],
["pump time nodes", "pumpnodes"],
["pump duration", "pumpduration"],
["time interval [minutes]", "timeinterval"],
["start: run demo", "rundemo"],
["cloud config", "cloudconfig"],
["cloud update", "cloudupdate"]
]


def get_conf_data():
    return conf_data


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


def load_url_config(urlApi ="http://www.octopusengine.org/api/hydrop/"):
    url_config = {}
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
    print('=' * 39)
    for ix in conf_data:
        try:
            # print(ix, cc[ix]) # dict{}
            print(" %25s - %s " % (ix[0], cc[ix[1]] ))
        except:
            Err_print_config = True
    print('=' * 39)

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