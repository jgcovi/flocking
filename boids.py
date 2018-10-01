#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 11:44:37 2018

@author: jgcovi
"""

import numpy as np

class Boids(object):

    MAX_POSITION = 10
    MIN_POSITION = -10

    def __init__(self, position, speed, color):
        self.position = position
        self.heading = np.random.rand()  # initial heading does not matter
        self.speed = speed
        self._color = color

    def get_position(self):
        return self.position

    def get_speed(self):
        return self.speed

    def speed_up(self):
        self.speed += 0.1

    def forward_one(self):
        self.position = [p + 1 for p in self.position]

    def set_heading(self, heading):
        self.heading = heading

    def cone_of_vision(self):
        raise NotImplementedError()


class Prey(Boids):

    def __init__(self, speed=0.5):
        position_x = np.random.rand()
        position_y = np.random.rand()
        self.cone = self.cone_of_vision()

        Boids.__init__(self, position=[position_x, position_y], speed=speed, color='yellow')

    def cone_of_vision(self, radius=1, angle=np.pi/1.5):
        return [radius, angle]


class Predator(Boids):

    def __init__(self, speed=0.5):
        position_x = np.random.rand()
        position_y = np.random.rand()
        self.cone = self.cone_of_vision()

        Boids.__init__(self, position=[position_x, position_y], speed=speed, color='red')

    def set_heading(self, heading):
        self.heading = heading

    def cone_of_vision(self, radius=1.5, angle=np.pi/3):
        """Predators have a smaller cone of vision than prey."""
        return [radius, angle]


class Flock(Prey):

    MIN_SEPARATION = 0.01

    def __init__(self, flock_size):

        self.flock_size = flock_size
        self.flock = np.array([Prey() for _ in range(flock_size)])
        self.flock_positions = np.array([boid.get_position() for boid in self.flock], dtype=Prey)

    def get_position(self):
        return np.array([boid.position for boid in self.flock])

    def get_speed(self):
        return np.array([boid.speed for boid in self.flock])

    def _separation(self):
        pass

    def _cohesion(self):
        pass

    def _alignment(self):
        pass
