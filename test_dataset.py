""" Run this module to generate the dataset for testing, randomly. """

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
__version__ = '2020.5.5'

TEST_DATASET_SIZE = 1000 # notice that the final dataset may be smaller
                         # after duplicate_removal
AVAILABLE_ROTATIONS = ['l', 'u', 'r', 'b', 'f', 'd', \
                        'l2', 'u2', 'r2', 'b2', 'f2', 'd2', \
                        'lr', 'ur', 'rr', 'br', 'fr', 'dr']

def datetime_(): # date and time will be the name of the dataset
    t = datetime.now().strftime("%y%m%d%H%M")
    return t

def touch(path, path2, filename): # path = 'test' or 'train'
    if not os.path.exists('datasets'):
        os.mkdir('datasets')
    if not os.path.exists('datasets/' + path):
        os.mkdir('datasets/' + path)
    if not os.path.exists('datasets/' + path + '/' + path2):
        os.mkdir('datasets/' + path + '/' + path2)
    if os.path.exists('datasets/' + path + '/' + path2 + '/' + filename + '.csv'):
        os.remove('datasets/' + path + '/' + path2 + '/' + filename + '.csv')
        f = open('datasets/' + path + '/' + path2 + '/' + filename + '.csv', 'x')
        f.close()
    else:
        f = open('datasets/' + path + '/' + path2 + '/' + filename + '.csv', 'x')
        f.close()

def generator(path, path2, filename): # rotating randomly & write combinations into dataset
    touch(path, path2, filename)
    cube = init_cube(RUBIK_SIZE)
    path = 'datasets/' + path + '/' + path2 + '/' + filename + '.csv'
    with open(path, 'w', newline='') as dataset:
        generator = csv.writer(dataset)
        for i in range(TEST_DATASET_SIZE):
            move = rd.choice(AVAILABLE_ROTATIONS)
            cube = turn(move, cube)
            row = rubik_to_array(cube, RUBIK_SIZE)
            row = np.append(row, rotating_notations(move))
            generator.writerow(row)

def duplicate_removal(path, path2, filename): # remove duplicate in datasets
    old_path = 'datasets/' + path + '/' + path2 + '/' + filename + '.csv'
    new_path = 'datasets/' + path + '/' + path2 + '/' + filename + '_cached.csv'
    shucopy(old_path, new_path)
    os.remove(old_path)
    touch(path, path2, filename)
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

def duplicate_removal_v2(path, path2, filename, size): # check only combinations, not full row
    old_path = 'datasets/' + path + '/' + path2 + '/' + filename + '.csv'
    new_path = 'datasets/' + path + '/' + path2 + '/' + filename + '_cached.csv'
    num_of_cols = size**2*6
    shucopy(old_path, new_path)
    os.remove(old_path)
    touch(path, path2, filename)
    with open(new_path, 'r') as clipboard, open (old_path, 'w') as final:
        cached = set()
        counter = 0
        for line in clipboard:
            if line[:num_of_cols] in cached:
                counter+=1
            if line[:num_of_cols] not in cached:
                cached.add(line[:num_of_cols])
                final.write(line)
    os.remove(new_path)
    return(counter)

if __name__ == '__main__':
    start = time()
    filename = datetime_()
    dir = 'test'
    dir2 = str(RUBIK_SIZE)
    generator(dir, dir2, filename)
    print("Done! \nTime elapsed = " + str(round((time() - start), 3)) + " seconds")
    duplicates = duplicate_removal_v2(dir, dir2, filename, RUBIK_SIZE)
    print(str(duplicates) + "/" + str(TEST_DATASET_SIZE) + " were duplicates " + \
        "and automatically removed.")
