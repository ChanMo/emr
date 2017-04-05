import serial
from directive import DIRECTIVE

class Ser(object):
    def __init__(self, dev):
        self.ser = serial.Serial(dev)

    def open(self):
        if not self.isOpen():
            self.ser.open()

    def close(self):
        if self.isOpen():
            self.ser.close()

    def turn_on(self, number):
        directive = DIRECTIVE[number*2]
        self.ser.write(directive)

    def turn_off(self, number):
        directive = DIRECTIVE[number*2 + 1]
        self.ser.write(directive)
