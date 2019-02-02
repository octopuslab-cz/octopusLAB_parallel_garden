
from micropython import const

# PIN as on octopusLAB Wemos ESP8266 IoTBoard1
BUILT_IN_LED = const(2)
HALL_SENSOR = const(8)

#I2C:
I2C_SCL_PIN = const(22)
I2C_SDA_PIN = const(21)

# SPI:
SPI_CLK_PIN  = const(18)
SPI_MISO_PIN = const(19)
SPI_MOSI_PIN = const(23)
SPI_CS0_PIN  = const(5)

ANALOG_PIN = const(36)
BUTT1_PIN = const(12)
PIEZZO_PIN = const(14)
WS_LED_PIN = const(15)
ONE_WIRE_PIN = const(13)
