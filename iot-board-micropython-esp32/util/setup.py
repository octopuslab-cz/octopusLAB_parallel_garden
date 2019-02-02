# this module is to setup your board throuhg REPL
# it's loaded in boot.py and provides function setup()
# user is questioned in interactive mode

#TODO DRY for filename
import time, uos
import ujson
import machine #datetime

devices = [
["oLAB Default","esp32"],
["oLAB Witty","esp8266"],
["oLAB Tickernator","esp8266"],
["oLAB BigDisplay3","esp8266"],
["oLAB RobotBoard1 v1","esp32"],
["oLAB RobotBoard1","esp32"],
["oLAB IoTBoard1","esp8266"],
["oLAB IoTBoard1","esp32"]
]

def deploy(url):
    import sys
    import os
    import lib.shutil as shutil
    import upip_utarfile as utarfile
    import urequests

    res = urequests.get(url)

    if not res.status_code == 200:
        return

    def dir_exists(path):
        try:
            os.stat(path)
            return True
        except:
            return False

    t = utarfile.TarFile(fileobj = res.raw)

    for f in t:
        print("Extracting {}: {}".format(f.type, f.name))
        if f.type == utarfile.DIRTYPE:
            if f.name[-1:] == '/':
                name = f.name[:-1]
            else:
                name = f.name

            if not dir_exists(name):
                os.mkdir(name)
        else:
            extracted = t.extractfile(f)
            shutil.copyfileobj(extracted, open(f.name, "wb"))

def setupMenu():
    print()
    print('=' * 30)
    print('        S E T U P')
    print('=' * 30)
    print("[ds]  - device setting")
    print("[sw]  - set wifi")
    print("[cw]  - connect wifi")
    print("[st]  - set time")
    print("[sd]  - system download >")
    print("(initial octopus modules)")
    print("[si]  - system info")
    print("[e]   - exit setup")

    print('=' * 30)
    sel = input("select: ")
    return sel

def setup():
    print("Hello, this will help you initialize your ESP")
    print("Press Ctrl+C to abort")
    print()

    # TODO improve this
    # prepare directory
    if 'config' not in uos.listdir():
       uos.makedirs('config')

    run= True
    while run:
        sele = setupMenu()

        if sele == "e":
            print("Setup - exit >")
            time.sleep_ms(2000)
            print("all OK, press CTRL+D to soft reboot")
            run = False

        if sele == "si": #system_info()
            from util.sys_info import sys_info
            sys_info()

        if sele == "ds":
            print("Device setting:")
            print("   board_type  | soc_type (system on the board)")
            i=0
            for di in devices:
               print(str(i)+": "+str(di[0]) + " | " + str(di[1]))
               i=i+1

            print()
            sd = input("select: ")
            #print(str(devices[int(sd)]))
            print("> " + str(devices[int(sd)][0]) + " | " + str(devices[int(sd)][1]))

            dc = {}
            dc['board_type'] = str(devices[int(sd)][0]) #input("Board type ('oLAB RobotBoard1' or 'oLAB IoTBoard1'): ")
            dc['soc_type'] = str(devices[int(sd)][1])   #input("SoC type ('esp32' or 'esp8266'): ")

            print("Writing to file config/device.json")
            with open('config/device.json', 'w') as f:
                ujson.dump(dc, f)
                # ujson.dump(wc, f, ensure_ascii=False, indent=4)

        if sele == "sw":
            print("Set WiFi >")
            print()
            wc = {}
            wc['wifi_ssid'] = input("SSID: ")
            wc['wifi_pass'] = input("PASSWORD: ")

            # TODO improve this
            if 'config' not in uos.listdir():
                uos.makedirs('config')

            print("Writing to file config/wifi.json")
            with open('config/wifi.json', 'w') as f:
                ujson.dump(wc, f)
                # ujson.dump(wc, f, ensure_ascii=False, indent=4)

        if sele == "cw":
              print("Connect WiFi >")
              from util.wifi_connect import read_wifi_config, WiFiConnect
              time.sleep_ms(1000)
              wifi_config = read_wifi_config()
              print("config for: " + wifi_config["wifi_ssid"])
              w = WiFiConnect()
              w.connect(wifi_config["wifi_ssid"], wifi_config["wifi_pass"])
              print("WiFi: OK")

        if sele == "st":
            print("Time setting >")
            rtc = machine.RTC()
            print(str(rtc.datetime()))
            setdatetime = input("input 6 numbers - format: RRRRR,M,D,wd,h,m > ")+(",0,0")
            dt_str = setdatetime.split(",")
            print(str(dt_str))
            dt_int = [int(numeric_string) for numeric_string in dt_str]
            rtc.init(dt_int)
            print(str(rtc.datetime()))

        if sele == "sd":
            print("System download > (initial octopus modules)")
            import upip
            print("Installing shutil")
            upip.install("micropython-shutil")
            print("Running deploy")
            #deplUrl = "http://iot.petrkr.net/olab/latest.tar"
            #deplUrl = "http://octopuslab.cz/download/latest.tar"
            deplUrl = "http://octopusengine.org/download/latest.tar"
            deploy(deplUrl)
