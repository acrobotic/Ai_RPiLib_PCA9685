#!/usr/bin/python

import time
import math
import smbus

# ===========================================================================
# PCA9685 Python Library
# Based on example Python Servo Code for Hobbytronics PWM/Servo board
# Author: MakerBro for ACROBOTIC Industries
# Date: 05/08/2016
# ===========================================================================

bus = smbus.SMBus(1)  # RPi V2 - for V1 RPi use SMBus(0)
I2C_ADDR  = 0x60
# RST | EXTCLK | AUTOINC | SLEEP | SUB1 | SUB2 | SUB3 | ALL
REG_MODE1       = 0x00  
REG_PRESC       = 0xFE
REG_LED0_ON_L   = 0x06
REG_LED0_ON_H   = 0x07
REG_LED0_OFF_L  = 0x08
REG_LED0_OFF_H  = 0x09

# Define a class for our servo functions
class Driver:
    def __init__(self, address):
        self.address = address
        self.duration_1ms = 0
        self.frequency = 0

    def setLowPowerMode(self, enable=True):
        if enable:
            # Low power mode. Oscillator off.
            bus.write_byte_data(self.address, REG_MODE1, 0x10)
        else:
            # TODO: need to read the register
            bus.write_byte_data(self.address, REG_MODE1, 0x00)

    def setExtClock(self, enable=True):
        if enable:
            self.setLowPowerMode(True)
            #  Write logic 1s to both the SLEEP and EXTCLK bits in MODE1.
            bus.write_byte_data(self.address, REG_MODE1, 0x50)
        else:
            pass # sticky bit so needs reset

    def setFreq(self, frequency):
        self.frequency = frequency
        self.duration_1ms = ((4096*frequency)/1000);  # This is 1ms duration
        prescale = 25000000.0   #25MHz Oscillator Clock
        prescale /= 4096.0
        prescale /= float(frequency)
        prescale -= 1.0
        prescale8 = int(math.floor(prescale + 0.5))
        self.setLowPowerMode(True)
        #self.setExtClock(True)
        bus.write_byte_data(self.address, REG_PRESC, prescale8) # set the prescaler
        self.setLowPowerMode(False)
        time.sleep(0.01)
        bus.write_byte_data(self.address, REG_MODE1, 0xA0)      # Set Auto-Increment on, enable restart

    def setPWM(self, channel, off_count, on_count=0x00):
        bus.write_byte_data(self.address, REG_LED0_ON_L+(4*channel), on_count & 0xFF)
        bus.write_byte_data(self.address, REG_LED0_ON_H+(4*channel), on_count >> 8)
        bus.write_byte_data(self.address, REG_LED0_OFF_L+(4*channel), off_count & 0xFF)
        bus.write_byte_data(self.address, REG_LED0_OFF_H+(4*channel), off_count >> 8) 

    def setOn(self, channel):
        bus.write_byte_data(self.address, REG_LED0_ON_H+(4*channel), 0x10)

    def setOff(self, channel):
        bus.write_byte_data(self.address, REG_LED0_OFF_H+(4*channel), 0x10)

# Create an instance of PWM Driver class
driver = Driver(I2C_ADDR)
driver.setFreq(1000)

pwm_enable = 1
pwm_direction = 0

#driver.setPWM(pwm_direction, 4095)
driver.setOn(pwm_direction)
driver.setPWM(pwm_enable, 512)
