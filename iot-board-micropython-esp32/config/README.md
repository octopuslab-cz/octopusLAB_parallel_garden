Configuration directory, please use .tpl, to create your versions of .json



Device config
-------------

This is important for corrects pinouts to be loaded automatically

Copy device.json.tpl to device.json
and edit wifi.json accordingly


Example:
{
  "board_type": "oLAB IoTBoard1",
  "soc_type": "esp32"
}


Board types:
- "oLAB RobotBoard1 v1"
- "oLAB RobotBoard1"
- "oLAB IoTBoard1"

SoC types:
- "esp32"
- "esp8266"


Wireless config
---------------

For wireless connectivity

Copy wifi.json.tpl to wifi.json
and edit wifi.json accordingly

Example:
{
  "wifi_ssid": "myap",
  "wifi_pass": "mypassword"
}


Playlist config
---------------

For managing which program will be executed

Example:
{
  "repeat": true,
  "auto_next": true,
  "next_delay_ms": 1000
}






TODO:
redo this in YAML
