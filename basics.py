""" This contains the mechanics of a rubik cube. """

import tensorflow as tf
import numpy as np
import math
import copy
from dependencies import *
from colorama import Fore, Back, Style

__author__ = 'Duy Cao'
__version__ = '20.5.3'

RUBIK_SIZE = 2  # means 2x2x2 rubik cube, modify this to change the size

def total_combinations(x):  # We assume that there is no rubik cube with size <= 1
    a = math.factorial(7)*3**6
    b = (24*2**10*math.factorial(12))**(x%2)
    c = math.factorial(24)**((x-2)/2)
    d = (math.factorial(24)/(math.factorial(4)**6))**(((x-2)/2)**2)
    combinations = int(a*b*c*d)
    return combinations

def init_cube(x):
    front = np.full((x,x), 'w')
    back = np.full((x,x), 'y')
    right = np.full((x,x), 'r')
    left = np.full((x,x), 'o')
    top = np.full((x,x), 'b')
    bottom = np.full((x,x), 'g')
    cube = [top, left, front, right, back, bottom]
    return cube
    # We use Western Color Scheme: White(w), Red(r), Blue(b), Yellow(y), Green(g),
    # and Orange(o)
    # A solved 2x2x2 rubik cube looks like this (front face is white):
    #        ______
    #       | b b |
    #       | b b |
    # -------------------------
    # | o o | w w | r r | y y |
    # | o o | w w | r r | y y |
    # -------------------------
    #       | g g |
    #       | g g |
    #       -------

def _test_cube(x):  #RUBIK_SIZE must >= 3
    cube = init_cube(x)
    cube[0][0,1], cube[0][1,0], cube[0][1,2], cube[0][2,1] = 'g', 'g', 'g', 'g'
    cube[1][0,1], cube[1][1,0], cube[1][1,2], cube[1][2,1] = 'r', 'r', 'r', 'r'
    cube[2][0,1], cube[2][1,0], cube[2][1,2], cube[2][2,1] = 'y', 'y', 'y', 'y'
    cube[3][0,1], cube[3][1,0], cube[3][1,2], cube[3][2,1] = 'o', 'o', 'o', 'o'
    cube[4][0,1], cube[4][1,0], cube[4][1,2], cube[4][2,1] = 'w', 'w', 'w', 'w'
    cube[5][0,1], cube[5][1,0], cube[5][1,2], cube[5][2,1] = 'b', 'b', 'b', 'b'
    return cube

def turn(x, rubik):  # including 18 basic rotations of a rubik cube

    copied = copy.deepcopy(rubik)

    if x == 'l':  # rotate left face clockwisely in 90 degrees
        for i in range(3):
            rubik[1] = np.rot90(rubik[1])
        rubik[0][:,0] = np.flipud(copied[4])[:,RUBIK_SIZE-1]
        rubik[2][:,0] = copied[0][:,0]
        rubik[5][:,0] = copied[2][:,0]
        rubik[4][:,RUBIK_SIZE-1] = np.flipud(copied[5])[:,0]

    if x == 'u':  # rotate top face clockwisely in 90 degrees
        for i in range(3):
            rubik[0] = np.rot90(rubik[0])
        rubik[1][0,:] = copied[2][0,:]
        rubik[2][0,:] = copied[3][0,:]
        rubik[3][0,:] = copied[4][0,:]
        rubik[4][0,:] = copied[1][0,:]

    if x == 'r':  # rotate right face closewisely in 90 degrees
        for i in range(3):
            rubik[3] = np.rot90(rubik[3])
        rubik[0][:,RUBIK_SIZE-1] = copied[2][:,RUBIK_SIZE-1]
        rubik[2][:,RUBIK_SIZE-1] = copied[5][:,RUBIK_SIZE-1]
        rubik[5][:,RUBIK_SIZE-1] = np.flipud(copied[4])[:,0]
        rubik[4][:,0] = np.flipud(copied[0])[:,RUBIK_SIZE-1]

    if x == 'f':  # rotate front face closewisely in 90 degrees
        for i in range(3):
            rubik[2] = np.rot90(rubik[2])
        rubik[0][RUBIK_SIZE-1,:] = np.fliplr(np.rot90(copied[1]))[0,:]
        rubik[1][:,RUBIK_SIZE-1] = np.flipud(np.rot90(copied[5]))[:,0]
        rubik[3][:,0] = np.flipud(np.rot90(copied[0]))[:,RUBIK_SIZE-1]
        rubik[5][0,:] = np.fliplr(np.rot90(copied[3]))[RUBIK_SIZE-1,:]

    if x == 'd':  # rotate bottom face closewisely in 90 degrees
        for i in range(3):
            rubik[5] = np.rot90(rubik[5])
        rubik[1][RUBIK_SIZE-1,:] = copied[4][RUBIK_SIZE-1,:]
        rubik[2][RUBIK_SIZE-1,:] = copied[1][RUBIK_SIZE-1,:]
        rubik[3][RUBIK_SIZE-1,:] = copied[2][RUBIK_SIZE-1,:]
        rubik[4][RUBIK_SIZE-1,:] = copied[3][RUBIK_SIZE-1,:]

    if x == 'b':  # rotate back face closewisely in 90 degrees
        for i in range(3):
            rubik[4] = np.rot90(rubik[4])
        rubik[0][0,:] = np.rot90(copied[3])[0,:]
        rubik[1][:,0] = np.rot90(copied[0])[:,0]
        rubik[3][:,RUBIK_SIZE-1] = np.rot90(copied[5])[:,RUBIK_SIZE-1]
        rubik[5][RUBIK_SIZE-1,:] = np.rot90(copied[1])[RUBIK_SIZE-1,:]

    if x == 'u2':  # rotate top face clockwisely in 90 degrees TWICE
        for f in range(2):
            turn('u',rubik)

    if x == 'd2':  # rotate bottom face clockwisely in 90 degrees TWICE
        for f in range(2):
            turn('d',rubik)

    if x == 'r2':  # rotate right face clockwisely in 90 degrees TWICE
        for f in range(2):
            turn('r',rubik)

    if x == 'f2':  # rotate front face clockwisely in 90 degrees TWICE
        for f in range(2):
            turn('f',rubik)

    if x == 'l2':  # rotate left face clockwisely in 90 degrees TWICE
        for f in range(2):
            turn('l',rubik)

    if x == 'b2':  # rotate back face clockwisely in 90 degrees TWICE
        for f in range(2):
            turn('b',rubik)

    if x == 'ur':  # rotate top face COUNTERCLOCKWISELY in 90 degrees
        for f in range(3):
            turn('u',rubik)

    if x == 'dr':  # rotate bottom face COUNTERCLOCKWISELY in 90 degrees
        for f in range(3):
            turn('d',rubik)

    if x == 'fr':  # rotate front face COUNTERCLOCKWISELY in 90 degrees
        for f in range(3):
            turn('f',rubik)

    if x == 'br':  # rotate back face COUNTERCLOCKWISELY in 90 degrees
        for f in range(3):
            turn('b',rubik)

    if x == 'lr':  # rotate left face COUNTERCLOCKWISELY in 90 degrees
        for f in range(3):
            turn('l',rubik)

    if x == 'rr':  # rotate right face COUNTERCLOCKWISELY in 90 degrees
        for f in range(3):
            turn('r',rubik)
    return rubik

def rotating_notations(x):
    if x == 'l':
        return 'left'
    if x == 'r':
        return 'right'
    if x == 'u':
        return 'top'
    if x == 'd':
        return 'bottom'
    if x == 'f':
        return 'front'
    if x == 'b':
        return 'back'
    if x == 'lr':
        return 'left-reversed'
    if x == 'rr':
        return 'right-reversed'
    if x == 'ur':
        return 'top-reversed'
    if x == 'dr':
        return 'bottom-reversed'
    if x == 'fr':
        return 'front-reversed'
    if x == 'br':
        return 'back-reversed'
    if x == 'l2':
        return 'left-twice'
    if x == 'r2':
        return 'right-twice'
    if x == 'u2':
        return 'top-twice'
    if x == 'd2':
        return 'bottom-twice'
    if x == 'f2':
        return 'front-twice'
    if x == 'b2':
        return 'back-twice'


def _test():
    x=total_combinations(RUBIK_SIZE)
    print('There are total ' + str(x) + ' combinations!')
    #y = init_cube(RUBIK_SIZE)
    test = _test_cube(RUBIK_SIZE)
    before = copy.deepcopy(test)
    #print("BEFORE")
    #visualizer(before, RUBIK_SIZE)
    after = turn('rr', test)
    #print("\n AFTER")
    #visualizer(after, RUBIK_SIZE)
    y = rubik_to_array(after, RUBIK_SIZE)[4]
    print(type(y))

if __name__ == '__main__':
    _test()
