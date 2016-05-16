#!/usr/bin/python

# ===========================================================================
# PCA9685 Python Library
# Based on example Python Servo Code for Hobbytronics PWM/Servo board
# Author: MakerBro for ACROBOTIC Industries
# Date: 05/08/2016
# ===========================================================================
import time
import math
import smbus
import RPi.GPIO as GPIO

bus = smbus.SMBus(1)  # RPi V2 - for V1 RPi use SMBus(0)
I2C_ADDR  = 0x60
# MODE1[7:0] RST | EXTCLK | AUTOINC | SLEEP | SUB1 | SUB2 | SUB3 | ALL
REG_MODE1           = 0x00
# MODE2[7:0] N/A | N/A | N/A | INVRT | OCH | OUTDRV | OUTNE[1:0]
REG_MODE2           = 0x01
REG_PRESC           = 0xFE
REG_LED0_ON_L       = 0x06
REG_LED0_ON_H       = 0x07
REG_LED0_OFF_L      = 0x08
REG_LED0_OFF_H      = 0x09
REG_LEDALL_ON_L     = 0xFA
REG_LEDALL_ON_H     = 0xFB
REG_LEDALL_OFF_L    = 0xFC
REG_LEDALL_OFF_H    = 0xFD

# Define a class for our servo functions
class Driver:
    CHANNEL_0  = 0
    CHANNEL_1  = 1
    CHANNEL_2  = 2
    CHANNEL_3  = 3
    CHANNEL_4  = 4
    CHANNEL_5  = 5
    CHANNEL_6  = 6
    CHANNEL_7  = 7
    CHANNEL_8  = 8
    CHANNEL_9  = 9
    CHANNEL_10 = 10
    CHANNEL_11 = 11
    CHANNEL_12 = 12
    CHANNEL_13 = 13
    CHANNEL_14 = 14
    CHANNEL_15 = 15

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
        self.duration_1ms = ((4096*frequency)/1000);  # This is 1ms duration (TODO)
        prescale = 25000000.0   #25MHz Oscillator Clock
        prescale /= 4096.0
        prescale /= float(frequency)
        prescale -= 1.0
        prescale8 = int(math.floor(prescale + 0.5))
        self.setLowPowerMode(True)
        bus.write_byte_data(self.address, REG_PRESC, prescale8) # set the prescaler
        self.setLowPowerMode(False)
        time.sleep(0.01)
        bus.write_byte_data(self.address, REG_MODE1, 0xA0)      # Set Auto-Increment on, enable restart

    def setExtClock(self):
        self.setLowPowerMode(True)
        self.setExtClock(True)
        self.setLowPowerMode(False)
        bus.write_byte_data(self.address, REG_MODE1, 0x80)      # Set enable restart

    def setPWM(self, channel, off_count, on_count=0x00):
        bus.write_byte_data(self.address, REG_LED0_ON_L+(4*channel), on_count & 0xFF)
        bus.write_byte_data(self.address, REG_LED0_ON_H+(4*channel), on_count >> 8)
        bus.write_byte_data(self.address, REG_LED0_OFF_L+(4*channel), off_count & 0xFF)
        bus.write_byte_data(self.address, REG_LED0_OFF_H+(4*channel), off_count >> 8) 

    def setOn(self, channel):
        bus.write_byte_data(self.address, REG_LED0_ON_H+(4*channel), 0x10)
        bus.write_byte_data(self.address, REG_LED0_OFF_H+(4*channel), 0x00)

    def setOff(self, channel):
        bus.write_byte_data(self.address, REG_LED0_ON_H+(4*channel), 0x00)
        bus.write_byte_data(self.address, REG_LED0_OFF_H+(4*channel), 0x10)

    def setAllOff(self):
        bus.write_byte_data(self.address, REG_LEDALL_ON_H, 0x00)
        bus.write_byte_data(self.address, REG_LEDALL_OFF_H, 0x10)

if __name__ == '__main__':
    # Create an instance of PWM Driver class
    driver = Driver(I2C_ADDR)
    driver.setFreq(1000)

    pwm_1 = driver.CHANNEL_0
    pwm_2 = driver.CHANNEL_1

    try:
       # while True:
        driver.setOn(pwm_1)
        driver.setPWM(pwm_2, 4095)
        time.sleep(60)
            #driver.setOff(pwm_1)
            #driver.setPWM(pwm_2, 4095)
            #time.sleep(10)
            #driver.setAllOff()
    except KeyboardInterrupt:
        print "Turning Off All Channels...!"
    finally:
        driver.setAllOff()
