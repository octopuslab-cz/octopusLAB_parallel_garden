# octopusLAB example - 2019
# simple dallas thermometer and oled test

from time import sleep, sleep_ms
from urandom import randint
from util.octopus import temp_init, get_temp, oled_init, w_connect, web_server
from util.display_segment import threeDigits
from util.iot_garden import fade_in, demo_relay, led_fet
from util.pinout import set_pinout
from lib.microWebSrv import MicroWebSrv
from machine import PWM, Pin

OLEDX = 128
OLEDY = 64
OLED_x0 = 3
OLED_ydown = OLEDY-7

def demo_run():
    fade_in(1024)
    demo_relay(2,5000)
    led_fet(0, 1000)

def displBar(oled, num, timb, anim, by = 58):
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
    time.sleep_ms(timb)    

def displBarSlimH(oled,val,ybh = 11): # horizontal    
    xbh = 2
    maxbv = 126
    oled.hline(xbh,ybh,maxbv,0)
    for ix in range(42):
        oled.fill_rect(xbh+ix*3,ybh,1,1,1)
    oled.hline(xbh,ybh,val,1) 
    oled.show()

def displMessage(mess,timm):
    try:
        oled.fill_rect(0,OLED_ydown-17,OLEDX,10,0)
        oled.text(mess, OLED_x0, OLED_ydown-17)
        oled.show()
        sleep_ms(timm*1000)
    except Exception as e:
       print("Err. displMessage2() Exception: {0}".format(e))


@MicroWebSrv.route('/led/pwm', "POST")
def _httpLedPwmSet(httpClient, httpResponse):
    print("LED PWM Call")

    data = httpClient.ReadRequestContent()
    print(data)

    if FET is None:
        httpResponse.WriteResponse(code=500, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = "MFET is not defined, check setup()")
        return
    
    try:
        value = int(data)
        FET.duty(value)
    except Exception as e:
        print("Exception: {0}".format(e))
        raise
    finally:
        httpResponse.WriteResponseOk(None)

    httpResponse.WriteResponse(code=204, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = None)

@MicroWebSrv.route('/relay', "POST")
def _httpRelaySet(httpClient, httpResponse):
    print("Relay Call")

    data = httpClient.ReadRequestContent()
    print(data)

    if RELAY is None:
        httpResponse.WriteResponse(code=500, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = "RELAY is not defined, check setup()")
        return
    
    try:
        value = int(data)
        RELAY.value(value)
    except Exception as e:
        print("Exception: {0}".format(e))
        raise
    finally:
        httpResponse.WriteResponseOk(None)

    httpResponse.WriteResponse(code=204, headers = None, contentType = "text/plain", contentCharset = "UTF-8", content = None)

# ======================
print ("Running MAIN")

pinout = set_pinout()

FET = None
if pinout.MFET_PIN is not None:
    FET = PWM(Pin(pinout.MFET_PIN), freq=2000)
    FET.duty(0)

RELAY = None
if pinout.RELAY_PIN is not None:
    RELAY = Pin(pinout.RELAY_PIN)

print("init > ")
t = temp_init()
oled = oled_init()
sleep(1)
oled.clear()

w_connect()
web_server()

print("test")
"""
displMessage("test LIGHT&PUMP",1)
for _ in range(9):
    randval = randint(1, 4000)
    valmap = map(randval, 0, 4000, 0, 125)
    displBarSlimH(oled, valmap, 11) # 0-120 / y
    time.sleep_ms(300)
    demo_run()
else:
    print("NO demo test") 
"""

print("start > ")

while True:
    temp  = get_temp(t[0], t[1])
    print(temp)
    temp10 = int(temp * 10)
    threeDigits(oled, temp10, True, True)
    sleep(3)
