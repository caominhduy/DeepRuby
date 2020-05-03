"""
Run this module to generate the training dataset.
"""

import numpy as np
import copy
import csv
import os
from datetime import datetime
from dependencies import *
from basics import *
import random as rd
from time import time
from shutil import copy as shucopy
from test_dataset import *

__author__ = 'Duy Cao'
__version__ = '2020.5.3'

TRAIN_DATASET_SIZE = 100000 # THE LARGER, THE BETTER (with a cost of time and memory)

def training_generator(path, path2, filename): # rotating randomly & write combinations into dataset
    touch(path, path2, filename)
    cube = init_cube(RUBIK_SIZE)
    path = 'datasets/' + path + '/' + path2 + '/' + filename + '.csv'
    with open(path, 'w', newline='') as dataset:
        generator = csv.writer(dataset)
        for i in range(TRAIN_DATASET_SIZE):
            move = rd.choice(AVAILABLE_ROTATIONS)
            cube = turn(move, cube)
            row = rubik_to_array(cube, RUBIK_SIZE)
            row = np.append(row, rotating_notations(move))
            generator.writerow(row)

if __name__ == '__main__':
    start = time()
    filename = datetime_()
    dir = 'train'
    dir2 = str(RUBIK_SIZE)
    training_generator(dir, dir2, filename)
    print("Done! \nTime elapsed = " + str(round((time() - start), 3)) + " seconds")
    duplicates = duplicate_removal(dir, dir2, filename)
    print(str(duplicates) + " duplicates were automatically removed.")
