"""this module is to load proper pinout per config"""
import json

def set_pinout():
    device_config = {}
    pinout = None

    try:
        with open('config/device.json', 'r') as f:
            d = f.read()
            f.close()
            device_config = json.loads(d)
    except:
        print("Device config 'config/device.json' does not exist, please run setup()")

    if device_config.get('board_type') == "oLAB default" and device_config.get('soc_type') == "esp32":
        import pinouts.olab_esp32_default as pinout

    if device_config.get('board_type') == "oLAB Tickernator" and device_config.get('soc_type') == "esp8266":
        import pinouts.olab_esp8266_tickernator as pinout

    if device_config.get('board_type') == "oLAB BigDisplay3" and device_config.get('soc_type') == "esp8266":
        import pinouts.olab_esp8266_big_display as pinout

    if device_config.get('board_type') == "oLAB RobotBoard1" and device_config.get('soc_type') == "esp32":
        import pinouts.olab_esp32_robot_board1 as pinout

    if device_config.get('board_type') == "oLAB RobotBoard1 v1" and device_config.get('soc_type') == "esp32":
        import pinouts.olab_esp32_robot_board1_v1 as pinout

    if device_config.get('board_type') == "oLAB IoTBoard1" and device_config.get('soc_type') == "esp8266":
        import pinouts.olab_esp8266_iot_board1 as pinout

    if device_config.get('board_type') == "oLAB IoTBoard1" and device_config.get('soc_type') == "esp32":
        import pinouts.olab_esp32_iot_board1 as pinout

    return pinout
