#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 15:53:33 2018

@author: jgcovi
"""
import numpy as np

from boids import Predator, Prey, Flock

def main():

    prey = Prey()
    predator = Predator()
    flock = Flock(4)

    print(prey.get_position())
    print(predator.get_position())

    print()
    print(flock)
    print(flock.get_position())
    print(flock.get_speed())

#if __name__ == 'main':
main()
