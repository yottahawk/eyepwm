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
    def __init__(self, radius = 0, centre = 0, vertical_channel = 0, horizontal_channel = 1):
        """ The constructor takes a horizontal and vertical channel as input, which correspond to which channel each servomotor is connected to on the Raspberry PI PWM Hat. 
        The 'radius' and 'centre' arguments are for the simulation model, which is currently not included in this codebase. 
        """

        # PWM Setup Variables
        self.eye                  = PCA9685(0x40) # Always use the default i2c address for the PWM hats
        self.__vert_ch            = vertical_channel
        self.__horiz_ch           = horizontal_channel
        self.__pwm_freq = 50 
        self.eye.set_pwm_freq(50)

        self.__pwm_bitres = 4096
        self.__pwm_scaler = self.__pwm_bitres * (1/self.__pwm_freq)
        # The PWM periods for a typical servomotor is between 1ms and 2ms, with 1.5ms being the middle of the useable range.        
        self.__pwm_period_min   = 10e-4 * self.__pwm_scaler # This is the minimum angle (1ms)
        self.__pwm_period_zero  = 15e-4 * self.__pwm_scaler # This angle is the middle of the servo range (1.5ms)
        self.__pwm_period_max   = 20e-4 * self.__pwm_scaler # This is the maximum angle (2ms)
        self.__pwm_period_range = self.__pwm_period_max - self.__pwm_period_min
        self.__servo_angle_max  =  80
        self.__servo_angle_min  = -80
        self.__servo_angle_range = self.__servo_angle_max - self.__servo_angle_min
        self.__eye_angle_max    =  30
        self.__eye_angle_min    = -30

        # Servo Position Tracking Variables (degrees)
        self.eye_vert_angle   = 0
        self.eye_horiz_angle  = 0      

        
        # Eye Simulation
        self.radius = radius
        self.centre = centre
        

    def step_vert_angle(self, step_size):
        """Advances the eye position by the "step_size" argument"""

        # First calculate the new angle
        self.eye_vert_angle += step_size
        self.eye_vert_angle = minmax(self.eye_vert_angle, eye)

        # Now map the new angle against a correction matrix, which accounts for the mechanism of the eye.
        servo_angle = map_eye_to_servo(self.eye_horiz_angle);

        # Convert the corrected angle into a PWM tick count and therefore duty cycle
        servo_pwm_period = conv_servo_angle_ms(int(servo_angle))

        # Apply this new duty cycle to the servomotor
        self.eye.set_pwm(self.__vert_ch, 0, servo_pwm_period)

        
    def step_horiz_angle(self, step_size):
        self.eye_horiz_angle += step_size
        self.eye_horiz_angle = minmax(self.eye_horiz_angle, eye)
        servo_angle = map_eye_to_servo(self.eye_horiz_angle);
        servo_pwm_period = conv_servo_angle_ms(int(servo_angle))
        self.eye.set_pwm(self.__horiz_ch, 0, servo_pwm_period)

        
    def get_vert_angle(self):
        return self.eye_vert_angle
    def get_horiz_ange(self):
        return self.eye_horiz_angle    

        
    def conv_servo_angle_ms(self, angle):
        """ Maps a servo angle to a number of ms PWM period required to move it to that position.
        A typical servo positioning system moves between -90 and 90 degress with periods between 1 and 2 ms.
        However, this library automatically takes the input angle and scales it to a position between the max servo range variables """

        scaled_angle = angle / self.__servo_angle_range
        return self.__pwm_period_min + (scaled_angle * self.__pwm_period_range)

    
    def map_eye_to_servo(self, angle):
        """ This function maps an input eye angle to a servo angle required to get the eye at that position. 
        This is required because of the linkage to the eye itself, which creates a mapping between the servo and eye angles. 
        This mapping may be different in vertical and horizontal angles. """
    
        # TODO
        return angle;

    def minmax(new_input, eye_or_servo):
        """ This function takes a new eye or servo position, and checks if it has exceeded either of the minimum or maximum values. 
        If the new value is outside the allowed range, limit it to the extreme value. 
        """

        if eye_or_servo == eye :
            if new_input > self.__eye_angle_max:
                new_input = self.__eye_angle_max
            elif new_input < self.__eye_angle_min:
                new_input = self.__eye_angle_min
        elif eye_or_servo == servo :
            if new_input > self.__servo_angle_max:
                new_input = self.__servo_angle_max
            elif new_input < self.__servo_angle_min:
                new_input = self.__servo_angle_min


    def vert_test(self):
        while True:
            self.eye_vert.set_pwm(self.__vert_ch, 0, int(self.__pwm_period_min))
            time.sleep(1)
            self.eye_vert.set_pwm(self.__vert_ch, 0, int( self.__pwm_period_zero))
            time.sleep(1)
            self.eye_vert.set_pwm(self.__vert_ch, 0, int(self.__pwm_period_max))
            time.sleep(2)

