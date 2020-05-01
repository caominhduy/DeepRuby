""" This file generates the dataset for testing, randomly. """

import numpy as np
import copy
import csv
import os
from datetime import datetime
from dependencies import *
from basics import *
import random as rd
from time import time

__author__ = 'Duy Cao'
__version__ = '2020.4.30'

TEST_DATASET_SIZE = 100000
AVAILABLE_ROTATIONS = ['l', 'u', 'r', 'b', 'f', 'd',
                        'l2', 'u2', 'r2', 'b2', 'f2', 'd2',
                        'lr', 'ur', 'rr', 'br', 'fr', 'dr',]

def datetime_(): # date and time will be the name of the dataset
    t = datetime.now().strftime("%y%m%d%H%M")
    return t

def touch(path, filename): # path = 'test' or 'train'
    if not os.path.exists('datasets'):
        os.mkdir('datasets')
    if not os.path.exists('datasets/' + path):
        os.mkdir('datasets/' + path)
    if os.path.exists('datasets/' + path + '/' + filename + '.csv'):
        os.remove('datasets/' + path + '/' + filename + '.csv')
        f = open('datasets/' + path + '/' + filename + '.csv', 'x')
        f.close()
    else:
        f = open('datasets/' + path + '/' + filename + '.csv', 'x')
        f.close()

def generator(filename): # rotating randomly and write into dataset
    cube = init_cube(RUBIK_SIZE)
    path = 'datasets/test/' + filename + '.csv'
    with open(path, 'w', newline='') as dataset:
        generator = csv.writer(dataset)
        for i in range(TEST_DATASET_SIZE):
            move = rd.choice(AVAILABLE_ROTATIONS)
            cube = turn(move, cube)
            row = rubik_to_array(cube, RUBIK_SIZE)
            generator.writerow(row)

def _main():
    start = time()
    filename = datetime_()
    touch('test', filename)
    generator(filename)
    print("Done! \nTime elapsed = " + str(round((time() - start), 3)) + " seconds")

_main()
