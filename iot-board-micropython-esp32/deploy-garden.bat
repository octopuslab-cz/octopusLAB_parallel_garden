@ECHO OFF
echo Welcome to basic octopusLAB script for ESP32 - Micropython!
REM pause

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

ampy -p  %PORT% put boot.py
REM ampy -p  %PORT% put ./octopus_robot_board.py

ampy -p  %PORT% mkdir pinouts
ampy -p  %PORT% put ./pinouts/olab_esp32_default.py pinouts/olab_esp32_default.py
ampy -p  %PORT% put ./pinouts/olab_esp32_robot_board1.py pinouts/olab_esp32_robot_board1.py
ampy -p  %PORT% put ./pinouts/olab_esp32_iot_board1.py pinouts/olab_esp32_iot_board1.py

ampy -p  %PORT% mkdir lib
ampy -p  %PORT% put ./lib/ssd1306.py lib/ssd1306.py
ampy -p  %PORT% put ./lib/temperature.py lib/temperature.py
ampy -p  %PORT% put ./lib/max7219.py lib/max7219.py
ampy -p  %PORT% put ./lib/max7219_8digit.py lib/max7219_8digit.py
ampy -p  %PORT% put ./lib/sm28byj48.py lib/sm28byj48.py
ampy -p  %PORT% put ./lib/tsl2561.py lib/tsl2561.py

ampy -p  %PORT% mkdir lib/bh1750
ampy -p  %PORT% put ./lib/bh1750/__init__.py lib/bh1750/__init__.py

ampy -p  %PORT% mkdir config
ampy -p  %PORT% put ./config/device.json config/device.json
ampy -p  %PORT% put ./config/garden.json config/garden.json

ampy -p  %PORT% mkdir util
ampy -p  %PORT% put ./util/setup.py util/setup.py
ampy -p  %PORT% put ./util/sys_info.py util/sys_info.py 
ampy -p  %PORT% put ./util/pinout.py util/pinout.py
ampy -p  %PORT% put ./util/octopus.py util/octopus.py
ampy -p  %PORT% put ./util/wifi_connect.py util/wifi_connect.py
ampy -p  %PORT% put ./util/display_segment.py util/display_segment.py
ampy -p  %PORT% put ./util/iot_garden.py util/iot_garden.py
ampy -p  %PORT% put ./util/octopus_lib.py util/octopus_lib.py

ampy -p  %PORT% mkdir util/led
ampy -p  %PORT% put ./util/led/__init__.py util/led/__init__.py

ampy -p  %PORT% mkdir util/buzzer
ampy -p  %PORT% put ./util/buzzer/__init__.py util/buzzer/__init__.py
ampy -p  %PORT% put ./util/buzzer/melody.py util/buzzer/melody.py
ampy -p  %PORT% put ./util/buzzer/notes.py util/buzzer/notes.py

ampy -p  %PORT% mkdir assets
ampy -p  %PORT% put ./assets/octopus_image.pbm assets/octopus_image.pbm 
ampy -p  %PORT% put ./assets/icons9x9.py assets/icons9x9.py

ampy -p  %PORT% put sensor_log.py main.py

ampy -p  %PORT% ls util

echo start:
echo >>> octopus()
