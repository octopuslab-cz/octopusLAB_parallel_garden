"""
sensor_log for #hydroponics IoT monitoring system
example usage of  SSD1306 OLED display
DS18B20 "Dallas" temperature sensor, light sensor BH1750, moisture sensor
ampy -p /COM5 put sensor_log.py main.py
alfa > beta
"""
ver = "26" # "0.ver" int > db
# last update 22.2.2019
print("sensor_log.py - version: 0." + ver)

import machine
from machine import Pin, PWM, Timer
import time, os, ubinascii
import urequests, json
import framebuf, math

from lib import ssd1306
from onewire import OneWire
from ds18x20 import DS18X20
from lib.bh1750 import BH1750
from lib.tsl2561 import TSL2561
from util.pinout import set_pinout
from util.buzzer import beep
from util.led import blink
from util.display_segment import *
from util.wifi_connect import read_wifi_config, WiFiConnect
from assets.icons9x9 import ICON_clr, ICON_wifi

Debug = True
place = "none"      # name group of IoT > load from config/garden.json
minute = 10         # 1/10 for data send
wifi_retries = 100  # for wifi connecting

isTemp = True
isLight = True
isMois = True
isPressure = False
isAD = False #TODO
isPH = False #TODO

# Defaults
tslLight = False
bhLight = False
bh2Light = False

pinout = set_pinout()
led = Pin(pinout.BUILT_IN_LED, Pin.OUT) # BUILT_IN_LED
pwM = Pin(pinout.PWM1_PIN, Pin.OUT)     # moisture
pin_an = Pin(pinout.I35_PIN, Pin.IN)
adcM = adc = machine.ADC(pin_an)
dspin = machine.Pin(pinout.ONE_WIRE_PIN)

garden_config = {}  # main system config - default/flash-json/web-cloud
if Debug: print("load config >")
try:
    with open('config/garden.json', 'r') as f:
        d = f.read()
        f.close()
        garden_config = json.loads(d)
    if Debug: print("from garden.json:")
    place = garden_config.get('place')

except:
        print("Device config 'config/garden.json' does not exist")
if Debug: print("place = " + place)
print()

if Debug: print("init i2c >")
i2c = machine.I2C(-1, machine.Pin(pinout.I2C_SCL_PIN), machine.Pin(pinout.I2C_SDA_PIN))

if Debug: print(" - scanning")
i2cdevs = i2c.scan()

if Debug: print(" - devices: {0}".format(i2cdevs))

# Determine what we have connected to I2C
isOLED = 0x3c in i2cdevs
bhLight = 0x23 in i2cdevs
bh2Light = 0x5c in i2cdevs
tslLight = 0x39 in i2cdevs

if Debug:
    print("OLED present: {0}".format(isOLED))
    print("Light meters\n  BH1730: {0}\n  BH1730 AUX: {1}\n  TSL2561: {2}".format(bhLight, bh2Light, tslLight))

if isOLED:
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    time.sleep_ms(100)

# magic constants )
aa = 16 # one segment size
y0 = 7  # y possition
x0 = aa-6
xb0 = 0 # display bar possition
yb0 = 58
ydown = 57
xt = 88 # display time possition
yt = 38

def add0(sn):
    ret_str=str(sn)
    if int(sn)<10:
       ret_str = "0"+str(sn)
    return ret_str

def get_hhmm():
    #print(str(rtc.datetime()[4])+":"+str(rtc.datetime()[5]))
    hh=add0(rtc.datetime()[4])
    mm=add0(rtc.datetime()[5])
    return hh+":"+mm

def get_moisture():
    pwM.value(1)
    time.sleep_ms(1000)
    s1 = adcM.read() #moisture sensor
    time.sleep_ms(1000)
    s2 = adcM.read() #moisture sensor

    s = int((s1+s2)/2)
    pwM.value(0)
    return(s)

def draw_icon(icon, posx, posy):
    if not isOLED:
        return

    for y, row in enumerate(icon):
        for x, c in enumerate(row):
            oled.pixel(x+posx, y+posy, c)

def get_eui():
    id = ubinascii.hexlify(machine.unique_id()).decode()
    return id #mac2eui(id)

# Define function callback for connecting event
def connected_callback(sta):
    global WSBindIP
    draw_icon(ICON_clr, 88 ,0)
    draw_icon(ICON_wifi, 88 ,0)
    print(sta.ifconfig())
    WSBindIP = sta.ifconfig()[0]

def disconnected_callback():
    if isOLED:
        draw_icon(ICON_clr, 88 ,0)
        oled.show()


def connecting_callback(attempt):
    if isOLED:
        draw_icon(ICON_wifi, 88 ,0)
        oled.show()

    blink(led, 50, 100)

    if isOLED:
        draw_icon(ICON_clr, 88 ,0)
        oled.show()

def connecting_timeout_callback():
    print("Failed connect to wifi: Timed out")

def w_connect():
    global wifi
    time.sleep_ms(1000)
    wifi_config = read_wifi_config()
    if Debug: print("config for: " + wifi_config["wifi_ssid"])
    wifi = WiFiConnect(wifi_config["wifi_retries"] if "wifi_retries" in wifi_config else wifi_retries )
    wifi.events_add_connecting(connecting_callback)
    wifi.events_add_connected(connected_callback)
    wifi.events_add_timeout(connecting_timeout_callback)
    wifi.events_add_disconnected(disconnected_callback)
    wifi_status = wifi.connect(wifi_config["wifi_ssid"], wifi_config["wifi_pass"])
    if Debug: print("WiFi: OK" if wifi_status else "WiFi: Error")

def oledImage(file):
    if not isOLED:
        return

    IMAGE_WIDTH = 63
    IMAGE_HEIGHT = 63

    with open('assets/'+file, 'rb') as f:
        f.readline() # Magic number
        f.readline() # Creator comment
        f.readline() # Dimensions
        data = bytearray(f.read())
        fbuf = framebuf.FrameBuffer(data, IMAGE_WIDTH, IMAGE_HEIGHT, framebuf.MONO_HLSB)
        # To display just blit it to the display's framebuffer (note you need to invert, since ON pixels are dark on a normal screen, light on OLED).
        oled.invert(1)
        oled.blit(fbuf, 0, 0)

    oled.text("Octopus", 66,6)
    oled.text("Lab", 82,16)
    oled.text("Micro", 74,35)
    oled.text("Python", 70,45)
    oled.show()

def blinkOledPoint():
    if not isOLED:
        return

    oled.fill_rect(x0,y0,5,5,1)
    oled.show()
    time.sleep_ms(1000)

    oled.fill_rect(x0,y0,5,5,0)
    oled.show()
    time.sleep_ms(2000)

urlMain = "http://www.octopusengine.org/iot17/add19req.php?type=iot&place=pp&device="
urlPOST = "http://www.octopusengine.org/iot17/add18.php"
header = {}
header["Content-Type"] = "application/x-www-form-urlencoded"

def bytearrayToHexString(ba):
    return ''.join('{:02X}'.format(x) for x in ba)

def sendData():
    try:
        # GET >
        #urlGET = urlMain + deviceID + "&type=temp1&value=" + str(tw)
        #print(urlGET)
        #req = urequests.post(url)
        if isTemp:
            ds.convert_temp()
            time.sleep_ms(750)
            for t in ts:
                temp = ds.read_temp(t)
                tw = int(temp*10)
                postdata_t = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, str(tw),"t{0}".format(bytearrayToHexString(t)[-6:]))
                res = urequests.post(urlPOST, data=postdata_t, headers=header)
                time.sleep_ms(1000)

        if isLight:
            if bhLight:
                numlux = sbh.luminance(BH1750.ONCE_HIRES_1)
                postdata_l = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, str(int(numlux)),"ligh1")
                res = urequests.post(urlPOST, data=postdata_l, headers=header)
                time.sleep_ms(1000)

            if bh2Light:
                numlux = sbh2.luminance(BH1750.ONCE_HIRES_1)
                postdata_l = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, str(int(numlux)),"ligh2")
                res = urequests.post(urlPOST, data=postdata_l, headers=header)
                time.sleep_ms(1000)

            if tslLight:
                numlux = tsl.read()
                postdata_l = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, str(int(numlux)),"ligh3")
                res = urequests.post(urlPOST, data=postdata_l, headers=header)
                time.sleep_ms(1000)

        if isMois:
            sM = get_moisture()
            postdata_l = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, str(int(sM)),"mois1")
            res = urequests.post(urlPOST, data=postdata_l, headers=header)

    except:
        displMessage("Err: send data",3)

def displMessage(mess,timm):
    if not isOLED:
        return

    oled.fill_rect(0,ydown,128,10,0)
    oled.text(mess, x0, ydown)
    oled.show()
    time.sleep_ms(timm*1000)

def displBar(by,num,timb,anim):
    if not isOLED:
        return

    if num>10: num = 10
    oled.fill_rect(xb0,by-1,128,5+2,0) # clear
    for i in range(10):               # 0
        oled.hline(xb0+i*13,by+2,9,1)
    if num > 0:
      for i in range(num):               # 1
        oled.fill_rect(xb0+i*13,by,10,5,1)
        if anim:
           oled.show()
           time.sleep_ms(30) # animation
    oled.show()
    time.sleep_ms(timb)

#----------------------------------------- init ------------------------------
if isOLED:
    oledImage("octopus_image.pbm")
    time.sleep_ms(2500)
    oled.invert(0)
    oled.fill(0)                # reset display

if isOLED:
    oled.text('octopusLAB', 0, 1)

if Debug: print("start - init")
deviceID = str(get_eui())
if Debug: print("> unique_id: "+ deviceID)

if isOLED:
    oled.text("wifi",99, 1)
    displMessage("wifi connect >",1)
w_connect()

displMessage("init >",1)

if Debug: print("init dallas temp >")
try:
    ds = DS18X20(OneWire(dspin))
    ts = ds.scan()

    if len(ts) <= 0:
        isTemp = False

    for t in ts:
        print(" --{0}".format(bytearrayToHexString(t)))
except:
    isTemp = False
print("Found {0} dallas sensors, temp active: {1}".format(len(ts), isTemp))

if bhLight:
    if Debug: print("init i2c BH1750 >")
    try:
        sbh = BH1750(i2c)
    except:
        pass

if bh2Light:
    if Debug: print("init i2c BH1750 AUX >")
    try:
        sbh2 = BH1750(i2c, addr=0x5C)
    except:
        pass

if tslLight:
    if Debug: print("init i2c TSL2561 >")
    try:
        tsl = TSL2561(i2c)
        tsl.integration_time(402)
    except:
        pass

it = 0
def timerSend():
    global it
    it = it+1
    if Debug: print(">"+str(it))

    if (it == 6*minute): # 6 = 1min / 60 = 10min
        if Debug: print("10 min. > send data:")
        sendData() # read sensors and send data
        it = 0

if Debug: print("time setup >")
rtc = machine.RTC() # real time
urltime="http://www.octopusengine.org/api/hydrop/get-datetime.php"
try:
   response = urequests.get(urltime)
   dt_str = (response.text+(",0,0")).split(",")
   print(str(dt_str))
   dt_int = [int(numeric_string) for numeric_string in dt_str]
   rtc.init(dt_int)
   print(str(rtc.datetime()))
except:
    print("Err. Setup time from WiFi")

tim1 = Timer(0)
tim1.init(period=10000, mode=Timer.PERIODIC, callback=lambda t:timerSend())

"""
tim1 = Timer(1)
tim1.init(mode=Timer.PERIODIC, period=1000)
tim.callback(timer2do)
"""
sendData() # first test sending

if Debug: print("start - loop")

if isOLED:
    displMessage("start > 0."+ver,1)

#log start > version
try:
    postdata_v = "device={0}&place={1}&value={2}&type={3}".format(deviceID, place, ver,"log_ver")
    res = urequests.post(urlPOST, data=postdata_v, headers=header)
    time.sleep_ms(200)
except:
    displMessage("Err: send data",3)

# ======================================= main loop ==========================
while True:
    if isOLED: # displ time
      oled.fill_rect(xt,yt,xt+50,yt+10,0)
      oled.text(get_hhmm(), xt, yt)
      oled.show()
    try:

        wifi.handle_wifi()

        if isLight:
            if bhLight:
                numlux = sbh.luminance(BH1750.ONCE_HIRES_1)
                print("BH:"+str(numlux))
                displBar(yb0,int(math.log10(numlux)*2),300,1)

            if bh2Light:
                numlux = sbh2.luminance(BH1750.ONCE_HIRES_1)
                print("BH AUX:"+str(numlux))
                displBar(yb0,int(math.log10(numlux)*2),300,1)

            if tslLight:
                numlux = tsl.read()
                print("TSL:"+str(numlux))
                displBar(yb0,int(math.log10(numlux)*2),300,1)

        if isTemp:
            ds.convert_temp()
            time.sleep_ms(750)
            for t in ts:
                temp = ds.read_temp(t)
                tw = int(temp*10)
                print("T({0}): {1}".format(bytearrayToHexString(t), str(tw/10)))
                if isOLED:
                    threeDigits(oled,tw,True,True)

        #if isMois: #only test
        #    s = get_moisture()
        #    print("M:"+str(s))

    except Exception as e:
        print("Exception: {0}".format(e))
        try:
            displMessage("Err: main loop",3)
        except:
            # In case OLED error, do not crash^M
            pass
    #blinkOledPoint()
    time.sleep_ms(1000)
