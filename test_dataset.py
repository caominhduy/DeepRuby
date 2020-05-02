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
from shutil import copy as shucopy

__author__ = 'Duy Cao'
__version__ = '2020.1.5'

TEST_DATASET_SIZE = 10000 # notice that the final dataset may be smaller
                         # after duplicate_removal
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

def generator(dir, filename): # rotating randomly & write combinations into dataset
    touch('test', filename)
    cube = init_cube(RUBIK_SIZE)
    path = 'datasets/' + dir + '/' + filename + '.csv'
    with open(path, 'w', newline='') as dataset:
        generator = csv.writer(dataset)
        for i in range(TEST_DATASET_SIZE):
            move = rd.choice(AVAILABLE_ROTATIONS)
            cube = turn(move, cube)
            row = rubik_to_array(cube, RUBIK_SIZE)
            generator.writerow(row)

def duplicate_removal(dir, filename): # remove duplicate in datasets
    old_path = 'datasets/' + dir + '/' + filename + '.csv'
    new_path = 'datasets/' + dir + '/' + filename + '_cached.csv'
    shucopy(old_path, new_path)
    os.remove(old_path)
    touch(dir, filename)
    with open(new_path, 'r') as clipboard, open (old_path, 'w') as final:
        cached = set()
        counter = 0
        for line in clipboard:
            if line in cached:
                counter+=1
            if line not in cached:
                cached.add(line)
                final.write(line)
    os.remove(new_path)
    return(counter)

def _main():
    start = time()
    filename = datetime_()
    generator('test', filename)
    print("Done! \nTime elapsed = " + str(round((time() - start), 3)) + " seconds")
    duplicates = duplicate_removal('test', filename)
    print(str(duplicates) + "/" + str(TEST_DATASET_SIZE) + " were duplicates " + \
        "and automatically removed.")

if __name__ == '__main__':
    _main()
