"""
This is octopusLab basic library for iotBoard PCB and esp32 soc
I2C / SPI / MOTORs / SERVO / PWM...
Edition: --- 2.1.2019 ---
"""
from micropython import const
# PIN as on octopusLAB Wemos ESP32 IoTBoard1
BUILT_IN_LED = const(2)
HALL_SENSOR = const(8)

#SPI:
SPI_CLK_PIN  = const(18)
SPI_MISO_PIN = const(19)
SPI_MOSI_PIN = const(23)
SPI_CS0_PIN  = const(5)

#I2C:
I2C_SCL_PIN = const(22)
I2C_SDA_PIN = const(21)

#---esp32---IoT board:
PIEZZO_PIN = const(27)  #14 //MOTOR_4A = const(27)
WS_LED_PIN = const(15)  #TDO
ANALOG_PIN = const(36)
ONE_WIRE_PIN = const(32) # = DEV1_PIN
RELAY_PIN = const(33)
MFET_PIN = const(14)

BUTT1_PIN = const(25) # up
BUTT2_PIN = const(12) # o #TDI
BUTT3_PIN = const(13) # dw #TCK

PWM1_PIN = const(17) #PWM/servo //pwr for moisture
PWM2_PIN = const(16)
PWM3_PIN = const(4)

DEV1_PIN = const(32)
DEV2_PIN = const(26)

#inputs:
I39_PIN = const(39)
I34_PIN = const(34)
I35_PIN = const(35) #analog in for moisture
