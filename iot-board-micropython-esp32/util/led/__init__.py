from time import sleep_ms

def blink(pin_obj, length_on=1000, length_off=1000):
    if length_off == 1000 and length_on != 1000:
        length_off = length_on
    pin_obj.value(1)
    sleep_ms(length_on)
    pin_obj.value(0)
    sleep_ms(length_off)
