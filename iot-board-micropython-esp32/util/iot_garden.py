# this module is to setup your board
# iotBoard for project parallel garden
#

import machine
from machine import Pin, PWM, ADC
import time, os, ubinascii
from util.pinout import set_pinout

pinout = set_pinout()

pwM = Pin(pinout.PWM1_PIN, Pin.OUT)     # moisture
pin_an = Pin(pinout.I35_PIN, Pin.IN)
adcM = adc = machine.ADC(pin_an)

pin_an = Pin(pinout.ANALOG_PIN, Pin.IN)
adc = machine.ADC(pin_an)

# ---------------- procedures
def getGardenLibVer():
    print("garden lib.ver: 26.2.2019")

def getADvolt(Debug): # AD > volts?
     an = adc.read()
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
