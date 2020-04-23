import tensorflow as tf
import numpy as np
import cv2 as cv
import math

"""
This contains the mechanics of a rubik cube
"""

RUBIK_SIZE = 2 # means 2x2x2 rubik cube, modify this to change the size

def total_combinations(x): # We assume that there is no rubik cube with size <= 1
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
    cube = top, left, front, right, back, bottom
    return cube[0]
    # We use Western Color Scheme: White(w), Red(r), Blue(b), Yellow(y), Green(g),
    # and Orange(o)
    # Example of a complete 2x2x2 rubik cube
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


#def visualization(s):

def main():
    x=total_combinations(RUBIK_SIZE)
    print('There are total ' + str(x) + ' combinations!')
    y = init_cube(RUBIK_SIZE)
    print(y)

main()
