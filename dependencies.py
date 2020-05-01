""" This contains supporting functions. """

import tensorflow as tf
import numpy as np
import math
import copy

from colorama import Fore, Back, Style

__author__ = 'Duy Cao'
__version__ = '2020.4.30'

def visualizer(rubik,size):  # Visualize a rubik cube as example in 'basics' module
    empty_matrix = np.full((size, size), ' ')
    for i in range(3):
        first = np.hstack((empty_matrix, rubik[0], empty_matrix, empty_matrix))
        second = np.hstack((rubik[1], rubik[2], rubik[3], rubik[4]))
        third = np.hstack((empty_matrix, rubik[5], empty_matrix))
    print(first)
    print(second)
    print(third)

def rubik_to_array(rubik, size): # cast rubik np multidimensional array into 1-D array
    new_array = np.array([])
    for y in range(6):
        for i in range(size):
            x = rubik[y][i]
            new_array = np.concatenate((new_array, x), axis=None)
    return new_array
