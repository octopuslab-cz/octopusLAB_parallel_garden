# this module is to setup your board
# iotBoard for project parallel garden
#

import machine
from machine import Pin, PWM, ADC
import time, os, ubinascii
import framebuf

# ---------------- procedures
def getOctopusLibVer():
    return "octopus lib.ver: 8.3.2019"

def printLog(i,s):
    print()
    print('-' * 30)
    print("[--- " + str(i) + " ---] " + s)    

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

def get_hhmm(rtc):
    hh=add0(rtc.datetime()[4])
    mm=add0(rtc.datetime()[5])
    return hh+":"+mm 

def blinkOledPoint(oled):
    oled.fill_rect(x0,y0,5,5,1)
    oled.show()
    time.sleep_ms(1000)

    oled.fill_rect(x0,y0,5,5,0)
    oled.show()
    time.sleep_ms(2000)

def oledImage(oled, file):

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
        
    oled.show()
