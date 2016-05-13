#!/usr/bin/python

import time
import math
import smbus

# ===========================================================================
# Example Python Servo Code for Hobbytronics PWM/Servo board
# http://www.hobbytronics.co.uk/pwm-servo
#
# Set servo position using format similar to Arduino where position
# is defined in degrees 0 to 180 with 90 being the center position
# 
# Pulse type is defined as 'standard' (0) generates pulse of 1ms to 2ms
#                          'extended' (1) generates pulse of 0.6ms to 2.4ms
# ===========================================================================

bus = smbus.SMBus(1)  # RPi V2 - for V1 RPi use SMBus(0)

# Define a class for our servo functions
class Driver:
    def __init__(self, address):
        self.address = address
        self.duration_1ms = 0
        self.frequency = 0

    def setLowPowerMode(self, enable=True):
        if enable:
            # Low power mode. Oscillator off.
            bus.write_byte_data(self.address, 0x00, 0x10)
        else:
            pass # need to read the register

    def setExtClock(self, enable=True):
        if enable:
            setLowPowerMode(True)
            #  Write logic 1s to both the SLEEP and EXTCLK bits in MODE1.
            bus.write_byte_data(self.address, 0x00, 0x50)
        else:
            pass # sticky bit so needs reset

    def setFreq(self, frequency):
        self.frequency = frequency
        self.duration_1ms = ((4096*frequency)/1000);  # This is 1ms duration
        prescale = 16000000.0
        prescale /= 4096.0
        prescale /= float(frequency)
        prescale -= 1.0
        prescale8 = int(math.floor(prescale + 0.5))
        bus.write_byte_data(self.address, 0xFE, prescale8) # set the prescaler
        time.sleep(0.01)
        bus.write_byte_data(self.address, 0x00, 0xA0)      # Set Auto-Increment on, enable restart

   def setPWM(self, channel, duration):
      bus.write_byte_data(self.address, 0x06+(4*channel), 0x00)
      bus.write_byte_data(self.address, 0x07+(4*channel), 0x00)
      bus.write_byte_data(self.address, 0x08+(4*channel), duration & 0xFF)
      bus.write_byte_data(self.address, 0x09+(4*channel), duration >> 8) 

# Create an instance of PWMServo class
driver = Driver(0x60)
driver.setFreq(100)

while (True):
   # Set servos 0,1,2 using standard pulse length
   driver.setPWM(0, 1024)
   driver.setPWM(1, 4096)
   time.sleep(2)
   driver.setPWM(0, 2048)
