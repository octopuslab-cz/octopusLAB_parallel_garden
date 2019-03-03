# this module is to setup your board
# iotBoard for project parallel garden
#
import machine
from machine import Pin, PWM, ADC
import time, os, ubinascii
from util.pinout import set_pinout

pinout = set_pinout()

pwM = Pin(pinout.PWM1_PIN, Pin.OUT)     # moisture
pin_adcM = Pin(pinout.I35_PIN, Pin.IN)
adcM = machine.ADC(pin_adcM)

pin_adc = Pin(pinout.ANALOG_PIN, Pin.IN)
adc = machine.ADC(pin_adc)

pin_relay = Pin(pinout.RELAY_PIN, Pin.OUT)
pin_fet = Pin(pinout.MFET_PIN, Pin.OUT)
pwm_fet = PWM(pin_fet, 500, 0)

 
def getGardenLibVer():
    return "garden lib.ver: 28.2.2019"

# ----------------

def getADvolt(Debug): # AD > volts?
     an1 = adc.read()
     an2 = adc.read()
     an = int((an1+an2)/2)
     if Debug:
         print("> analog RAW: " + str(an))
         # TODO improve mapping formula, doc: https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/adc.html
         print("volts: {0:.2f} V".format(an/4096*10.74), 20, 50)
     return an

def get_moisture():
    pwM.value(1)
    time.sleep_ms(1000)
    s1 = adcM.read() #moisture sensor
    time.sleep_ms(1000)
    s2 = adcM.read()
    time.sleep_ms(1000)
    s3 = adcM.read()

    s = int((s1+s2+s3)/3)
    pwM.value(0)
    return(s)

def fade_in(p, r, m):
     # pin - range - multipl
     for i in range(r):
          p.value(0)
          time.sleep_us((r-i)*m*2) # multH/L *2
          p.value(1)
          time.sleep_us(i*m)

def fade_out(p, r, m):
     # pin - range - multipl
     for i in range(r):
          p.value(1)
          time.sleep_us((r-i)*m)
          p.value(0)
          time.sleep_us(i*m*2)    

def relay(how):
        pin_relay.value(how)

def demo_relay(number=2, delay=3000):
    for _ in range (0, number):
        relay(1)
        time.sleep_ms(delay)
        relay(0)
        time.sleep_ms(delay)

def led_fet(duty, delay):
    pwm_fet.duty(duty)
    time.sleep_ms(delay)

def demo_run():
    # Demo intensity
    delayF = 500
    led_fet(1, delayF)
    led_fet(128, delayF)
    led_fet(512, delayF)
    led_fet(1023, delayF)
    led_fet(0, 2000)

    # demo Relay
    demo_relay(2,3000)
