# this module is to setup your board
# iotBoard for project parallel garden
#

import machine
from machine import Pin, PWM, ADC
import time, os, ubinascii

# ---------------- procedures
def getOctopusLibVer():
    print("octopus lib.ver: 27.2.2019")

def bytearrayToHexString(ba):
    return ''.join('{:02X}'.format(x) for x in ba)

def add0(sn): # 1 > 01
    ret_str=str(sn)
    if int(sn)<10:
       ret_str = "0"+str(sn)
    return ret_str

def get_eui():
    id = ubinascii.hexlify(machine.unique_id()).decode()
    return id #mac2eui(id)
