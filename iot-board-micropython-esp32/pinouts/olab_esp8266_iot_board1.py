
from micropython import const

# PIN as on octopusLAB Wemos ESP8266 IoTBoard1
BUILT_IN_LED = const(2)

BUTT1_PIN = 25 # up
BUTT2_PIN = 12 # o
BUTT3_PIN = 13 # dw

PIEZZO_PIN = 14
WS_LED_PIN = 15 #wemos gpio14 = d5
ONE_WIRE_PIN = 13

# I2C:
I2C_SCL_PIN=5 #gpio5=d1
I2C_SDA_PIN=4 #gpio4=d2

# SPI:
SPI_CLK_PIN  = const(18)
SPI_MISO_PIN = const(19)
SPI_MOSI_PIN = const(23)
SPI_CS0_PIN  = const(5)
