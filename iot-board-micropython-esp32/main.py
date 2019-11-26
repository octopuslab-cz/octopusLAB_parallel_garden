"""
sensor_log > iot_hydrop2
for #hydroponics IoT monitoring and control system - Parallel garden 2 (pg2)
- SSD1306 OLED display
- DS18B20 Dallas temperature sensor [C]
- BH1750 light sensor [Lux]
- moisture sensor and next A/D (light/temp) [RAW]
control: 
PWM LED and relay for water pump

ampy -p /COM6 put ./hydroponics/main.py main.py

[1] boot
[2] init/env.setup
[3] device config
[4] procedures / timer
[5] connect to netw.
[6] start main loop
"""

from time import sleep, sleep_ms
from math import log10
from urandom import randint
from machine import Pin, UART, RTC, Timer
from util.pinout import set_pinout
from util.octopus import getFree, map, printLog, printTitle, i2c_init, oled_init, time_init, getVer, get_hhmm, w
from hydroponics.send_data import send_data_post

ver = 0.55 # int(*100) > db
# last update 3.11.2019 
getFree(True)

# --------------------------------
printLog(1,"boot device >")
pinout = set_pinout()
led_numpin = pinout.BUILT_IN_LED # BUILT_IN_LED
dspin = Pin(pinout.ONE_WIRE_PIN)  # Dallas temperature
button3 = Pin(pinout.BUTT3_PIN, Pin.IN, Pin.PULL_UP)
#button3 = Pin(0, Pin.IN, Pin.PULL_UP) # test - boot pin
rtc = RTC() # real time
tim1 = Timer(0)     # for main 10 sec timer 
Debug = True

print("sensor_log2 - version: " + str(ver))
print(getVer())
#print(getGardenLibVer())
#deviceID = str(get_eui())

startLight = 0
stopLight = 1


sleep(1)
if not button3.value():
    from util.octopus import web_server
    print("Starting webserver > ")
    try:
        w()
        web_server()
    except Exception as e:
       print("timeDisplay() Exception: {0}".format(e))
       # todo:  Exception: memory allocation failed

    print("> stop main program")
    while True:
        sleep(10)


def timeDisplay():
    xt = 88 # display time possition
    yt = 38
    if not isOLED:
        return
    try:
       oled.fill_rect(xt,yt,40,12,0)
       oled.text(get_hhmm(), xt, yt)
       oled.show()
    except Exception as e:
       print("timeDisplay() Exception: {0}".format(e))


def tempDisplay(temp):
    tw = int(temp*10)
    # print("T({0}): {1}".format(bytearrayToHexString(t), str(tw/10)))
    if isOLED:
        threeDigits(oled,tw,True,True)


def displMessage(mess,timm=0.1):
    ydown = 57
    x0 = 5
    if not isOLED:
        return
    try:
        oled.fill_rect(0,ydown,128,10,0)
        oled.text(mess, x0, ydown)
        oled.show()
        sleep(timm)
    except Exception as e:
       print("displMessage() Exception: {0}".format(e)) 


def displBarSlimH(val,ybh = 11): # horizontal
    xbh = 2
    maxbv = 126
    oled.hline(xbh,ybh,maxbv,0)
    for ix in range(42):
        oled.fill_rect(xbh+ix*3,ybh,1,1,1)
    oled.hline(xbh,ybh,val,1) 
    oled.show()


def displBar(num, timb = 10, anim = False, by = 58):
    xb0 = 0 # display bar possition
   
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
    sleep_ms(timb)


def check_point(num, mess):
    printLog(num, mess)
    displMessage(mess)
    getFree(True)

def send_data():
    if ts:
        temp = int(ts.get_temp()*10)
        print(send_data_post("temp",temp), str(temp))
        sleep(1)

    if ios.get("mois"):
        mois1 = get_moisture()
        print(send_data_post("mois1",mois1), str(mois1))
        sleep(1)

    if sbh:
        light = 0 # todo
        sleep(1)
        try:
            light = int(sbh.luminance(BH1750.ONCE_HIRES_1))
            print(send_data_post("ligh1",light), str(light))
        except:
            pass

it = 0 # every 10 sec.
def timerSend():
    global it
    it = it + 1
    print(">" + str(it))

    if (it == 6*minute): # 6 = 1min / 60 = 10min
        if Debug: print("10 min. > send data:")
        send_data() # read sensors and send data
        it = 0 


def timer_init():
    printTitle("timer init > stop: tim1.deinit()")
    tim1.init(period=10000, mode=Timer.PERIODIC, callback=lambda t:timerSend())


def sensorsDisplay():
    if ts:
        try:
            temp = ts.get_temp()
        except Exception as e:
            print("Error reading dallas temperature")
            temp = 99.9

        tempDisplay(temp)

    if sbh:
        #light = randint(1, 10) # test
        #displBar(light)
        numlux = sbh.luminance(BH1750.ONCE_HIRES_1) 
        displBar(int(log10(numlux+1)*2)) 


def runAction(): # todo: fix
    # --- light
    global prewLight, pumpStat, oldLightIntensity

    hh=int(rtc.datetime()[4])
    mm=int(rtc.datetime()[5])

    print(">=startL: "+ str(startLight) + " :: <stopL: " + str(stopLight) + " --- now:"+ str(hh))
    
    if ((hh >= startLight) and (hh < stopLight)):
        if prewLight:
            print("> light on")
            # displMessage("light ON",1)
            if (oldLightIntensity != lightIntensity):
                pwmLed.freq(2000)
                pwmLed.duty(lightIntensity)
                displMessage("light:" + str(lightIntensity),1)                
                oldLightIntensity = lightIntensity
                print("change intensity: "+ str(lightIntensity))

        else:    
            print("> light on START")
            displMessage("light ON START",2) 
            # pwm_fet(lightIntensity, 2000) # 1023 # max 255=1/4 512=1/2 ...
            pwm_fade_in(pwmLed, lightIntensity)
            prewLight = True 
            oldLightIntensity = lightIntensity
            
    else: 
        print("> light off") 
        # displMessage("light OFF",1)
        pwmLed.duty(0)
        prewLight = False 
    
    # --- pump
    dayM = hh*60 + mm
    #try 

    for nodeM in pumpNodes:
        nodeMin = int(nodeM)*60
        # if Debug: print("dayMinutes: "+ str(dayM) + " :?: " + str(nodeMin) + " relay/pump Status: " + str(pumpStat))
        # print(str(nodeMin))
        if (dayM == nodeMin) and (pumpStat == 0):
            print("relay ON")
            displMessage("relay ON",1)
            relayPump.value(1)
            pumpStat = 1

        if (dayM == nodeMin + pumpDurat) and (pumpStat == 1):
            print("relay OFF")
            displMessage("relay OFF",1) 
            relayPump.value(0)
            pumpStat = 0
    #except:
    #    print("runAction() > ERR.pump") 

def button3Action():
    print("test button3")
    from util.buzzer.melody import jingle1
    piezzo.play_melody(jingle1)


# --------------------------------
printLog(2,"init/env.setup >")
from hydroponics.config import load_config, load_url_config, print_config, load_env_setup, print_env_setup
# extern config edit: ctr+c -> config.setup()
from config import Config
keys = ["startlight","stoplight","lightintensity","pumpnodes","pumpduration","timeinterval"]
config = Config("garden", keys)

# test
ios = load_env_setup()
printTitle("env.setup")
print_env_setup(ios)
# print(es["relay"])
i2c = i2c_init()

if ios.get("led"):
    from util.led import Led
    led = Led(led_numpin)
    led.blink()

piezzo = None
if ios.get('piezzo'): # todo: fix second init
    from util.buzzer import Buzzer
    piezzo = Buzzer(pinout.PIEZZO_PIN)

isOLED = False
if ios.get("oled"):
    print(">>> oled_init")
    from assets.icons9x9 import ICON_clr, ICON_wifi
    from util.display_segment import threeDigits
    isOLED = True
    try:
        oled = oled_init()
        sleep(1)
        oled.clear()
        displMessage("version: " + str(ver),1)
        for _ in range(5):
            randval = randint(1, 4000)
            valmap = map(randval, 0, 4000, 0, 125)
            displBarSlimH(valmap, 11) # 0-120 / y
            sleep(0.2)

        displBarSlimH(0, 11)
    except:
        print("Err.oled")
        isOLED = False

ts = None
if ios.get("temp"):
    print(">>> temp_init")
    from util.octopus import temp_init
    ts = temp_init() # ts := temp sensor
    sensorsDisplay()


if ios.get("mois"):
    print(">>> moisture_init")
    from machine import ADC
    from hydroponics.iot_garden import get_moisture
    pwM = Pin(pinout.PWM1_PIN, Pin.OUT)     # moisture
    pin_adcM = Pin(pinout.I35_PIN, Pin.IN)
    adcM = ADC(pin_adcM)
    if ios.get("mois"):
        adcM.adc.atten(ADC.ATTN_2_5DB)
        

relayPump = None
if ios.get("relay"):
    print(">>> relay_init")
    from util.iot import Relay
    relayPump = Relay()
    relayPump.value(1)
    sleep(1)
    relayPump.value(0)


pwmLed = None
if ios.get("fet"):
    print(">>> pwm_init")
    from hydroponics.iot_garden import pwm_init, pwm_fade_in
    pwmLed = pwm_init()
    pwm_fade_in(pwmLed, 1000)
    pwmLed.duty(0)


sbh = None
if ios.get("light"):
    print(">>> light sensor init")
    from lib.bh1750 import BH1750
    try:
        sbh = BH1750(i2c)
        testLight = int(sbh.luminance(BH1750.ONCE_HIRES_1))
        print("light > " + str(testLight))
    except:
        pass

# --------------------------------
check_point(3,"device config")
cf = load_config() # from file
print_config(cf)
minute = cf["timeinterval"]
startLight = cf["startlight"]
stopLight = cf["stoplight"]
prewLight = False
oldLightIntensity = 0
lightIntensity = cf["lightintensity"]

pumpNodes = cf["pumpnodes"]
if type(pumpNodes) is str:
    print("convert string pumpnodes to list (array) >")
    try:
        pumpNodes = list(pumpNodes[1:-1].split(",")) # string "[a,b]" to list [a,b]
    except Exception as e:
       print("timeDisplay() Exception: {0}".format(e))
    print(pumpNodes)

pumpDurat = cf["pumpduration"]
pumpStat = 0
sleep(1)

# --------------------------------
check_point(5,"connect to netw.")
try:
    oled.text('octopusLAB', 0, 1)
    oled.text("wifi",99, 1)
    oled.draw_icon(ICON_clr, 88 ,0)
    oled.draw_icon(ICON_wifi, 88 ,0) 
    cw = w()
    time_init()
    timeDisplay()
except:
    oled.draw_icon(ICON_clr, 88 ,0)
    displMessage("Err.w_connect")

uc = load_url_config() # from "web"
try:
    print(uc["version"]) # print(uc["pumpnodes"][1])
    print_config(uc)
except:
    print("Err.url_config")


printLog(6,"start main loop >")
displMessage("")
timer_init()
getFree(True)

print(send_data_post("pg2_ver",int(ver*100)))
sleep(2)
send_data() # firts test send data


# ============================= main loop ==========================
while True:
    try:
        # wifi.handle_wifi()
        sensorsDisplay()
        runAction()
        timeDisplay()

        sleep(0.2)

        if not button3.value():
            print("1 > butt3")
            displMessage("Basic info >",2)
            button3Action()

    except Exception as e:
       print("timeDisplay() Exception: {0}".format(e))
       sleep(1)
