
# from util.sys_info import sys_info
# sys_info()

import machine
import os, ubinascii
import gc #mem_free

rtc = machine.RTC() # real time

def get_eui():
    id = ubinascii.hexlify(machine.unique_id()).decode()
    return id #mac2eui(id)

def add0(sn):
    ret_str=str(sn)
    if int(sn)<10:
       ret_str = "0"+str(sn)
    return ret_str

def get_hhmm():
    #print(str(rtc.datetime()[4])+":"+str(rtc.datetime()[5]))
    hh=add0(rtc.datetime()[4])
    mm=add0(rtc.datetime()[5])
    return hh+":"+mm

def sys_info():
   print("> unique_id: "+str(get_eui()))
   #print("--- MAC: "+str(mac2eui(get_eui())))
   print("> uPy version: "+str(os.uname()[3]))
   #print("> octopus() ver: " + ver)
   try:
        with open('config/device.json', 'r') as f:
            d = f.read()
            f.close()
            print("> config/device: " + d)
            # device_config = json.loads(d)
   except:
        print("Device config 'config/device.json' does not exist, please run setup()")

   gc.collect()
   print("> mem_free: "+str(gc.mem_free()))
   print("> flash: "+str(os.statvfs("/")))
   print("> flash free: "+str(int(os.statvfs("/")[0])*int(os.statvfs("/")[3])))
   print("> machine.freq: "+str(machine.freq()))
   print("> active variables:")
   print(dir())
   print("> datetime RAW: "+str(rtc.datetime()))
