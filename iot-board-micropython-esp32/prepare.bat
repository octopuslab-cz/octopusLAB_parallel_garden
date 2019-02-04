@ECHO OFF
echo Welcome to basic octopusLAB script for ESP32 - Micropython!

REM --- TODO documentation
REM --- TODO check arguments

REM Setup your COM port
if %1.==. ( 
 SET /p PORT="Enter COM port for conection to the device. " 
) else ( SET PORT=%1
)

echo your port is: %PORT%

if %1.==. (
 echo "Please only execute in with ampy installed"
 pause
)


REM To skip the following commands, put "REM" before them:

ampy -p  %PORT% ls

@ECHO ON

echo "boot prepare"
ampy -p  %PORT% put boot_prepare.py boot.py

echo "config:"
ampy -p  %PORT% mkdir config
ampy -p  %PORT% put ./config/device.json config/device.json

echo "Lib:"
ampy -p  %PORT% mkdir lib

echo "Util:"
ampy -p  %PORT% mkdir util
ampy -p  %PORT% put ./util/setup.py util/setup.py
ampy -p  %PORT% put ./util/sys_info.py util/sys_info.py
ampy -p  %PORT% put ./util/wifi_connect.py util/wifi_connect.py

echo "ok - start: setup() in Mircopython"