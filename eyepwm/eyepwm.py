#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 16:55:05 2018

@author: Harry Callahan
"""

import numpy
from pyquaternion import *

class eyepwm:

    # Constructor for the eye class
    def __init__(self, radius, centre):

        # wlogger.log_info("Initialising Eye")

        # Radius of eye
        self.radius = radius
        self.centre = centre

        # latitudes & longitudes
        self.lats = 50
        self.longs = 50

        self.user_theta = 0
        self.user_height = 0
        self.x_angle_rad = 0
        self.y_angle_rad = 0
        self.angle_rad_limit = 0.7

    def step_x(self, step_size):

        self.x_angle_rad += step_size

        if self.x_angle_rad > self.angle_rad_limit:
            self.x_angle_rad = self.angle_rad_limit
        elif self.x_angle_rad < -self.angle_rad_limit:
            self.x_angle_rad = -self.angle_rad_limit
        else:
            rot_x = Quaternion(axis=[1.0, 0.0, 0.0], angle=step_size).normalised
            self.current_quaternion *= rot_x

    def step_y(self, step_size):

        self.y_angle_rad += step_size

        if self.y_angle_rad > self.angle_rad_limit:
            self.y_angle_rad = self.angle_rad_limit
        elif self.y_angle_rad < -self.angle_rad_limit:
            self.y_angle_rad = -self.angle_rad_limit
        else:
            rot_y = Quaternion(axis=[0.0, 1.0, 0.0], angle=step_size).normalised
            self.current_quaternion *= rot_y
