from time import sleep_ms

def play_tone(pwm_pin, freq, length, volume=50):
    # continuously
    pwm_pin.duty(volume)
    pwm_pin.freq(freq)
    sleep_ms(length)

def beep(p,f,t):  # port,freq,time
    #pwm0.freq()  # get current frequency
    p.freq(f)     # set frequency
    #pwm0.duty()  # get current duty cycle
    p.duty(512)   # set duty cycle
    sleep_ms(t)
    p.duty(0)
    #b.deinit()

def play_melody(pwm_pin, melody, volume=50):
    for note in melody:
        if note == 0:
            pwm_pin.duty(0)
        else:
            pwm_pin.duty(volume)
            pwm_pin.freq(note)
        sleep_ms(150)
