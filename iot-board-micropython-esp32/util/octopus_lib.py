# this module is to setup your board
# iotBoard for project parallel garden
#

import machine
from machine import Pin, PWM, ADC
import time, os, ubinascii
import framebuf

# ---------------- procedures
def getOctopusLibVer():
    return "octopus lib.ver: 10.3.2019"

def printLog(i,s):
    print()
    print('-' * 30)
    print("[--- " + str(i) + " ---] " + s)  

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)      

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

def oledInfoMess(oled, imm, tim, yup = 10):    
    oled.fill_rect(0,yup,128,64-yup,0) # clear 
    oled.text(imm[0], 3,12)
    oled.text(imm[1], 3,23)
    oled.text(imm[2], 3,34)
    oled.text(imm[3], 3,45)        
    oled.text(imm[4], 5,55) 
    oled.show() 
    time.sleep_ms(tim)
    oled.fill_rect(0,yup,128,64-yup,0)     

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

def displBarSlimV(oled, val, xbv = 0): # vertical 2 / 125
    ybv = 10
    maxbv = 21    
    oled.vline(xbv,ybv,maxbv,0)
    for iy in range(7):
        oled.fill_rect(xbv+1,ybv+iy*3,1,1,1)

    oled.vline(xbv,ybv,val,1) 
    oled.show() 