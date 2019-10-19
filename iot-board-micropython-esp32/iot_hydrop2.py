"""
sensor_log > iot_hydrop2
for #hydroponics IoT monitoring and control system
- SSD1306 OLED display
- DS18B20 "Dallas" temperature sensor
- BH1750 light sensor
- moisture sensor and next A/D (light/temp)
control: 
PWM LED and relay for water pump
"""

from time import sleep
from machine import Pin, PWM, ADC, UART, RTC, Timer
from util.pinout import set_pinout 
from util.octopus import getFree, printLog, printTitle, oled_init, time_init, getVer, get_hhmm, w

ver = "0.51" # int(*100) > db
# last update 20.10.2019 
getFree(True)


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


def check_point(num, mess):
    printLog(num, mess)
    displMessage(mess)
    getFree(True)


it = 0 # every 10 sec.
def timerSend():
    global it
    it = it+1
    print(">"+str(it))

    if (it == 6*minute): # 6 = 1min / 60 = 10min
        if Debug: print("10 min. > send data:")
        #sendData() # read sensors and send data
        it = 0 


def timer_init():
    printTitle("timer init > stop: tim1.deinit()")
    tim1.init(period=10000, mode=Timer.PERIODIC, callback=lambda t:timerSend())


# --------------------------------
printLog(1,"boot device >")
pinout = set_pinout()
led_numpin = pinout.BUILT_IN_LED # BUILT_IN_LED
dspin = Pin(pinout.ONE_WIRE_PIN)  # Dallas temperature
#button3 = Pin(pinout.BUTT3_PIN, Pin.IN, Pin.PULL_UP)
button3 = Pin(0, Pin.IN, Pin.PULL_UP) # test - boot pin
rtc = RTC() # real time
tim1 = Timer(0)     # for main 10 sec timer 

print("sensor_log2 - version: " + ver)
print(getVer())
#print(getGardenLibVer())
#deviceID = str(get_eui())

sleep(1)
# --------------------------------
printLog(2,"init/env.setup >")
from hydroponics.config import load_config, load_url_config, print_config, load_env_setup, print_env_setup

# test
es = load_env_setup()
printTitle("env.setup")
print_env_setup(es)
# print(es["relay"])

if es["led"]:
    from util.led import Led
    led = Led(led_numpin)
    led.blink()

isOLED = False
if es["oled"]:
    from assets.icons9x9 import ICON_clr, ICON_wifi
    isOLED = True
    try:
        oled = oled_init()
        sleep(1)
        oled.clear()
        displMessage("version: "+ver,2)
    except:
        isOLED = False

# --------------------------------
check_point(3,"device config")
cf = load_config() # from file
print_config(cf)
minute = cf["timeinterval"]
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
# ============================= main loop ==========================
while True:

    #wifi.handle_wifi()
    timeDisplay()
    #runAction()
    sleep(0.2)
    #sensorsDisplay()    

    if not button3.value():
        print("1 > butt3")
        displMessage("Basic info >",2)
        #butt3Action()
 