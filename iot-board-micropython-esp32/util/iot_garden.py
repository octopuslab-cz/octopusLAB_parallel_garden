# this module is to setup your board
# iotBoard for project parallel garden
#

import machine
from machine import Pin, PWM, ADC
import time, os, ubinascii
# ---------------- procedures
def getGardenLibVer():
    print("garden lib.ver: 26.2.2019")

def getADvolt(adc, Debug): # AD > volts?
     an = adc.read()
     if Debug:
         print("> analog RAW: " + str(an))
         # TODO improve mapping formula, doc: https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/adc.html
         print("volts: {0:.2f} V".format(an/4096*10.74), 20, 50)
     return an
