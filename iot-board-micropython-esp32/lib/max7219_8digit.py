# Licence: GPLv3
# Copyright 2017 Paul Dwerryhouse <paul@dwerryhouse.com.au>

CHAR_MAP = {
    '0': 0x7e, '1': 0x30, '2': 0x6d, '3': 0x79,
    '4': 0x33, '5': 0x5b, '6': 0x5f, '7': 0x70,
    '8': 0x7f, '9': 0x7b, 'a': 0x77, 'b': 0x1f,
    'c': 0x4e, 'd': 0x3d, 'e': 0x4f, 'f': 0x47,
    'g': 0x7b, 'h': 0x37, 'i': 0x30, 'j': 0x3c,
    'k': 0x57, 'l': 0x0e, 'm': 0x54, 'n': 0x15,
    'o': 0x1d, 'p': 0x67, 'q': 0x73, 'r': 0x05,
    's': 0x5b, 't': 0x0f, 'u': 0x1c, 'v': 0x3e,
    'w': 0x2a, 'x': 0x37, 'y': 0x3b, 'z': 0x6d,
    'A': 0x77, 'B': 0x1f, 'C': 0x4e, 'D': 0x3d,
    'E': 0x4f, 'F': 0x47, 'G': 0x7b, 'H': 0x37,
    'I': 0x30, 'J': 0x3c, 'K': 0x57, 'L': 0x0e,
    'M': 0x54, 'N': 0x15, 'O': 0x1d, 'P': 0x67,
    'Q': 0x73, 'R': 0x05, 'S': 0x5b, 'T': 0x0f,
    'U': 0x1c, 'V': 0x3e, 'W': 0x2a, 'X': 0x37,
    'Y': 0x3b, 'Z': 0x6d, ' ': 0x00, '-': 0x01,
    '\xb0': 0x63, '.': 0x80
}

REG_NO_OP           = 0x00
REG_DIGIT_BASE      = 0x01
REG_DECODE_MODE     = 0x09
REG_INTENSITY       = 0x0a
REG_SCAN_LIMIT      = 0x0b
REG_SHUTDOWN        = 0x0c
REG_DISPLAY_TEST    = 0x0f

class Display:

    def __init__(self, spi, ss, intensity=7):
        self.spi = spi
        self.ss = ss
        self.buffer = bytearray(8)
        self.intensity = intensity
        self.reset()

    def reset(self):
        self.set_register(REG_DECODE_MODE, 0)
        self.set_register(REG_INTENSITY, self.intensity)
        self.set_register(REG_SCAN_LIMIT, 7)
        self.set_register(REG_DISPLAY_TEST, 0)
        self.set_register(REG_SHUTDOWN, 1)

    def set_register(self, register, value):
        self.ss.value(0)
        self.spi.write(bytearray([register, value]))
        self.ss.value(1)

    def decode_char(self, c):
        d = CHAR_MAP.get(c)
        return d if d != None else ' '

    def write_to_buffer(self, s):
        l = len(s)
        if l < 8:
            s = "%-8s" % s
        for i in range(0,8):
            self.buffer[7-i] = self.decode_char(s[i])

    def display(self):
        for i in range(0,8):
            self.set_register(REG_DIGIT_BASE + i, self.buffer[i])

    def intensity(self, i):
        self.send(self.INTENSITY, i)
