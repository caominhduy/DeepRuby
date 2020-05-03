""" Let's do some training"""
""" Some of the codes were taken directly from TensorFlow Tutorial Documentation"""

import numpy as np
import tensorflow as tf
import copy
import csv
import os
from datetime import datetime
from dependencies import *
from basics import *
import random as rd
from time import time
from shutil import copy as shucopy
from train_dataset import TRAIN_DATASET_SIZE
from test_dataset import TEST_DATASET_SIZE, AVAILABLE_ROTATIONS
import functools

__author__ = 'Duy Cao'
__version__ = '2020.5.3'

TRAIN_DATASET_PATH = get_latest_file('datasets/train/' + str(RUBIK_SIZE))
TEST_DATASET_PATH = get_latest_file('datasets/test/' + str(RUBIK_SIZE))

def get_column_name(size):
    columns = []
    for i in ['top', 'left', 'front', 'right', 'back', 'bottom']:
        for x in range(RUBIK_SIZE**2):
            columns.append(i + '_' + str(x))
    columns.append('previous_move')
    return columns

def get_dataset(file_path):
    dataset = tf.data.experimental.make_csv_dataset(
        file_path,
        batch_size = 3,
        column_names=get_column_name(RUBIK_SIZE),
        label_name='previous_move',
        header=False,
        num_epochs=1,
        shuffle=True,
        shuffle_buffer_size = 1000,
        ignore_errors=True)
    return dataset

def show_batch(dataset):
  for batch, label in dataset.take(1):
    for key, value in batch.items():
      print("{:20s}: {}".format(key,value.numpy()))

if __name__ == "__main__":
    train_data = get_dataset(TRAIN_DATASET_PATH)
    test_data = get_dataset(TEST_DATASET_PATH)
    show_batch(train_data)
