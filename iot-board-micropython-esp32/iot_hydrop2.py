"""
sensor_log > iot_hydrop2
for #hydroponics IoT monitoring and control system
- SSD1306 OLED display
- DS18B20 "Dallas" temperature sensor
- BH1750 light sensor
- moisture sensor and next A/D (light/temp)
control: 
PWM LED and relay for water pump

ampy -p /COM6 put ./hydroponics/iot_hydrop2.py main.py
"""

from time import sleep, sleep_ms
from urandom import randint
from machine import Pin, UART, RTC, Timer
from util.pinout import set_pinout 
from util.octopus import getFree, map, printLog, printTitle, oled_init, time_init, getVer, get_hhmm, w
from hydroponics.send_data import send_data_post

ver = "0.51" # int(*100) > db
# last update 20.10.2019 
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

print("sensor_log2 - version: " + ver)
print(getVer())
#print(getGardenLibVer())
#deviceID = str(get_eui())

startLight = 0
stopLight = 1

def timeDisplay():
    xt = 88 # display time possition
    yt = 38
    if not isOLED:
        return
    try:
       oled.fill_rect(xt,yt,xt+50,yt+10,0)
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
    if ios["temp"]:
        temp = int(get_temp(*ts)*10)
        print(send_data_post("temp",temp), str(temp))
        sleep(1)

    if ios["light"]: # must exist: ios 0 or 1
        light = 0 # todo
        sleep(1)

it = 0 # every 10 sec.
def timerSend():
    global it
    it = it+1
    print(">"+str(it))

    if (it == 6*minute): # 6 = 1min / 60 = 10min
        if Debug: print("10 min. > send data:")
        sendData() # read sensors and send data
        it = 0 


def timer_init():
    printTitle("timer init > stop: tim1.deinit()")
    tim1.init(period=10000, mode=Timer.PERIODIC, callback=lambda t:timerSend())


def sensorsDisplay():
    if ios["temp"]:
        temp = get_temp(*ts)
        tempDisplay(temp)

        light = randint(1, 10) # test
        displBar(light)


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
        if Debug: print("dayMinutes: "+ str(dayM) + " :?: " + str(nodeMin) + " relay/pump Status: " + str(pumpStat))
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
    

sleep(1)
# --------------------------------
printLog(2,"init/env.setup >")
from hydroponics.config import load_config, load_url_config, print_config, load_env_setup, print_env_setup

# test
ios = load_env_setup()
printTitle("env.setup")
print_env_setup(es)
# print(es["relay"])

if ios["led"]:
    from util.led import Led
    led = Led(led_numpin)
    led.blink()

isOLED = False
if ios["oled"]:
    print(">>> oled_init")
    from assets.icons9x9 import ICON_clr, ICON_wifi
    from util.display_segment import threeDigits
    isOLED = True
    try:
        oled = oled_init()
        sleep(1)
        oled.clear()
        displMessage("version: "+ver,1)
        for _ in range(5):
            randval = randint(1, 4000)
            valmap = map(randval, 0, 4000, 0, 125)
            displBarSlimH(valmap, 11) # 0-120 / y
            sleep(0.2)

        displBarSlimH(0, 11)
    except:
        print("Err.oled")
        isOLED = False

if ios["temp"]:
    print(">>> temp_init")
    from util.octopus import temp_init, get_temp
    ts = temp_init() # ts temp sensor
    temp = get_temp(*ts)
    tempDisplay(temp)


if ios["relay"]:
    print(">>> relay_init")
    from hydroponics.iot_garden import relay_init # relay.value(x)
    relayPump = relay_init()
    relayPump.value(1)
    sleep(1)
    relayPump.value(0)


if ios["fet"]:
    print(">>> pwm_init")
    from hydroponics.iot_garden import pwm_init, pwm_fade_in
    pwmLed = pwm_init()
    pwm_fade_in(pwmLed, 1000)
    pwmLed.duty(0)

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
pumpDurat = cf["pumpduration"]
pumpStat = 0
sleep(1)

# --------------------------------
check_point(5,"connect to netw.")
oled.text("wifi",99, 1)
oled.draw_icon(ICON_clr, 88 ,0)
oled.draw_icon(ICON_wifi, 88 ,0) 
try:
    w()
    time_init()
    timeDisplay()
except:
    oled.draw_icon(ICON_clr, 88 ,0)
    displMessage("Err.w_connect")

cw = load_url_config() # from "web"
print(cw["version"]) # print(cw["pumpnodes"][1])
print_config(cw)


printLog(6,"start main loop >")
displMessage("")
timer_init()
getFree(True)
send_data() # firts test send data
# ============================= main loop ==========================
while True:

    #wifi.handle_wifi()
    timeDisplay()
    runAction()
    sleep(0.3)
    sensorsDisplay()

    if not button3.value():
        print("1 > butt3")
        displMessage("Basic info >",2)
        #butt3Action()
 