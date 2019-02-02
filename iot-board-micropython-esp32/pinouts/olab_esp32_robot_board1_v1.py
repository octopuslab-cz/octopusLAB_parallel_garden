"""
This is octopusLab basic library for robotBoard PCB
I2C / SPI / MOTORs / SERVO / PWM...
Edition: --- 31.10.2018 ---
Installation:
ampy -p /dev/ttyUSB0 put ./octopus_robot_board.py
"""

from micropython import const

# PIN as on octopusLAB ESP32 RobotBoard
# ESP32 pinout setup:
BUILT_IN_LED = const(2)
##WS_LED_PIN 13          # Robot Board v2
WS_LED_PIN = const(13)   # Robot Board v1 - WS RGB ledi diode
ONE_WIRE_PIN = const(32)  #one wire (for Dallas temperature sensor)

#I2C:
I2C_SCL_PIN = const(22)
I2C_SDA_PIN = const(21)

#SPI:
SPI_CLK_PIN  = const(18)
SPI_MISO_PIN = const(19)
SPI_MOSI_PIN = const(23)
SPI_CS0_PIN  = const(5)

# DC motors
MOTOR_12EN = const(25)
# Select version of robot board
##MOTOR_34EN 13          # Robot Board v2
MOTOR_34EN = const(15)   # Robot Board v1
MOTOR_1A = const(26)
MOTOR_2A = const(12)
MOTOR_3A = const(14)
MOTOR_4A = const(27)

#PWM/servo:
PWM1_PIN = const(17)
PWM2_PIN = const(16)
PWM3_PIN = const(4)
#pwm duty for servo:
SERVO_MIN = const(38)
SERVO_MAX= const(130)

#inputs:
I39_PIN = const(39)
I34_PIN = const(34)
I35_PIN = const(35)

#main analog input (for power management)
ANALOG_PIN = const(36)
PIEZZO_PIN = const(5)
