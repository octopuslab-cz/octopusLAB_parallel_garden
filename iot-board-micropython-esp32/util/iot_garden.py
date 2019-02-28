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

def demo_relay(number=2, delay=2000):
    for _ in range (0, number):
        pin_relay.value(1)
        time.sleep_ms(delay)
        pin_relay.value(0)
        time.sleep_ms(delay)

def demo_fet(duty, delay):
    pwm_fet.duty(duty)
    time.sleep_ms(delay)


def demo_run():
    # Demo intensity
    demo_fet(1, 2000)
    demo_fet(128, 2000)
    demo_fet(512, 2000)
    demo_fet(1023, 2000)
    demo_fet(0, 2000)

    # demo Relay
    demo_relay(delay=5000)
