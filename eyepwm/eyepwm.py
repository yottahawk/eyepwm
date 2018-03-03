#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 16:55:05 2018

@author: Harry Callahan

https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code
https://github.com/adafruit/Adafruit_Python_PCA9685
https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/overview
"""

from Adafruit_PCA9685 import PCA9685
import time
import numpy

class eyepwm:

    # Constructor for the eye class
    def __init__(self, radius, centre, vertical_channel = 0, horizontal_channel = 1):

        # PWM Setup Variables
        self.eye                          = PCA9685(0x40) # Always use the default i2c address for the PWM hats
        self.eye_vert.set_pwm_freq(50)
        self.eye_horiz.set_pwm_freq(50)
        self.vert_ch                   = vertical_channel
        self.horiz_ch                 = horizontal_channel

        self.pos_1ms =        8e-4 / ( 20e-3 / 4096)
        self.pos_1p5ms = 15e-4 / ( 20e-3 / 4096)
        self.pos_2ms =      22e-4 / ( 20e-3 / 4096)               

        # Eye Position Tracking Variables (degrees)
        self.eye_vert_angle = 0
        self.eye_horiz_angle = 0
        self.__eye_angle_max = 30
        self.__eye_angle_min = -30

        # 
        
        # Eye Simulation
        self.radius = radius
        self.centre = centre

    def step_vert_angle(self, step_size):
        """Advances the eye position by the "step_size" argument"""

        # First calculate the new angle
        self.eye_vert_angle += step_size
        if self.eye_vert_angle > self.__eye_angle_max:
            self.eye_vert_angle = self.__eye_angle_max
        elif self.eye_vert_angle < -self.__eye_angle_min:
            self.eye_vert_angle = -self.__eye_angle_min

        # Now map the new angle against a correction matrix, which accounts for the mechanism of the eye.

        # Convert the corrected angle into a PWM tick count and therefore duty cycle
        self.eye_vert.set_pwm(self.vert_channel, 0, self.conv_angle_ticks(self.eye_vert_angle))

        
    def step_horiz_angle(self, step_size):

        self.eye_horiz_angle += step_size
        if self.eye_horiz_angle > self.__eye_angle_max:
            self.eye_horiz_angle = self.__eye_angle_max
        elif self.eye_horiz_angle < -self.__eye_angle_min:
            self.eye_horiz_angle = -self.__eye_angle_min

    def conv_angle_ticks(self, angle):
        """ Maps the angle of the eye position to a servo rotation (0 to 180) by outputting a tick count, 
        where the fraction of ticks between 0 and 4096 defines the servo position. 
        0% duty results in an angle of -60, while 100% (4096) results in an angle of 60. """

        scaler = 4096 / 120
        ticks = 2048 + scaler*angle
        return ticks

    def vert_test(self):
        while True:
            self.eye_vert.set_pwm(self.vert_channel, 0, int(self.pos_1ms))
            time.sleep(1)
            self.eye_vert.set_pwm(self.vert_channel, 0, int( self.pos_1p5ms))
            time.sleep(1)
            self.eye_vert.set_pwm(self.vert_channel, 0, int(self.pos_2ms))
            time.sleep(2)
