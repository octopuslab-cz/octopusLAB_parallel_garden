from micropython import const

# PIN as on octopusLAB Witty ESP8266
BUILT_IN_LED = const(2)

LED_RED = const(15)
LED_GRE = const(12)
LED_BLU = const(13)

ANALOG_PIN = const(0) #A0 - LDR - photo resistor
BUTT1_PIN = const(14)

#---
PIEZZO_PIN = const(14)
WS_LED_PIN = const(16) 
ONE_WIRE_PIN = const(16) #

# I2C:
I2C_SCL_PIN = const(5) # gpio5=d1
I2C_SDA_PIN = const(4) # gpio4=d2

# SPI:
SPI_CLK_PIN  = const(18)
SPI_MISO_PIN = const(19)
SPI_MOSI_PIN = const(23)
SPI_CS0_PIN  = const(5)
