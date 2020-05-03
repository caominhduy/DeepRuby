""" This contains supporting functions. """

import tensorflow as tf
import numpy as np
import math
import copy
import os
from colorama import Fore, Back, Style

__author__ = 'Duy Cao'
__version__ = '2020.5.3'

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

def array_to_rubik(dummy, size, array): # basically this reverses rubik_to_array
    six_faces = np.reshape(array, (6, size**2))
    for i in range(6):
        dummy[i] = np.reshape(six_faces[i], (size, size))
    return dummy

def get_latest_file(dir):
    """
    list all the datasets by name (already named by date)
    and return the name of the lastest.
    """
    files = os.listdir(dir)
    new_files = []
    for file in files:
        new_file = file.replace('.csv', '')
        new_files.append(new_file)
    return dir + '/' + max(new_files) + '.csv'


if __name__ == '__main__':
    x = get_latest_file('datasets/train/2')
    print(x)
