"""
Credits:
    - Few LOCs were copied and modified from TensorFlow's Tutorial Documentation
"""

import numpy as np
import tensorflow as tf
import copy
import csv
import os, sys
from datetime import datetime
from dependencies import *
from basics import *
import random as rd
from shutil import copy as shucopy
from train_dataset import TRAIN_DATASET_SIZE
from test_dataset import *
import functools
import pandas as pd

__author__ = 'Duy Cao'
__version__ = '2020.5.7'

COLORS_DICT = {'b': 0, 'o': 1, 'w': 2, 'r': 3, 'y': 4, 'g': 5}

ROTATIONAL_DICT = {'left': 0, 'right': 1, 'top': 2, 'bottom': 3, 'front': 4, 'back': 5,\
    'left-reversed': 6, 'right-reversed': 7, 'top-reversed': 8, 'bottom-reversed': 9,\
    'front-reversed': 10, 'back-reversed': 11, 'left-twice': 12, 'right-twice': 13,\
    'top-twice': 14, 'bottom-twice': 15, 'front-twice': 16, 'back-twice': 17}

train_dataset_path = get_latest_file('datasets/train/' + str(RUBIK_SIZE))
test_dataset_path = get_latest_file('datasets/test/' + str(RUBIK_SIZE))


def get_column_name(size): # get column names for datasets (because top rows do not)
    columns = []
    for i in ['top', 'left', 'front', 'right', 'back', 'bottom']:
        for x in range(RUBIK_SIZE**2):
            columns.append(i + '_' + str(x))
    columns.append('previous_move')
    return columns

column_names = get_column_name(RUBIK_SIZE)

def get_vocab_list(): # create a nested dictionary of column name, color tile, and encoding integer
    dict = {}
    for name in column_names[:len(column_names)-1]:
        dict[name] = COLORS_DICT
    dict['previous_move'] = ROTATIONAL_DICT
    return dict

vocab_list = get_vocab_list()

# Load datasets as pandas dataframe
df_train = pd.read_csv( #training dataframe
    train_dataset_path,
    header=None,
    names = column_names,
    skip_blank_lines=True
    )

df_test = pd.read_csv( #testing dataframe
    test_dataset_path,
    header=None,
    names = column_names,
    skip_blank_lines=True
    )
#print(df_train.loc[0], y_train.loc[0]) # the first line

# Integer encoding
df_train.replace(vocab_list, inplace=True)
df_test.replace(vocab_list, inplace=True)
print(df_train.head())
# pop out the label column
y_train = df_train.pop('previous_move')
y_test = df_test.pop('previous_move')

# Load tensorflow datasets from pandas dataframes
def read_dataset_from_dataframe(col=column_names[:len(column_names)-1]):
    ds_train = tf.data.Dataset.from_tensor_slices((df_train[col].values, y_train.values)).shuffle(1000)
    ds_test = tf.data.Dataset.from_tensor_slices((df_test[col].values, y_test.values)).shuffle(1000)
    return ds_train, ds_test

ds_train, ds_test = read_dataset_from_dataframe()

for feat, targ in ds_train.take(5):
    print(f'Features: {feat}, Target: {targ}')

#for feat in ds_train.take(5):
#    print(feat)

def get_compiled_model():
  model = tf.keras.Sequential([
    tf.keras.layers.Dense(1000, activation='sigmoid'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1000, activation='sigmoid'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(100, activation='softmax'),
    tf.keras.layers.Dense(1)
  ])

  model.compile(optimizer='rmsprop',
                loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False),
                metrics=['accuracy'])
  return model

model = get_compiled_model()
model.fit(ds_train, epochs=2)

test_loss, test_accuracy = model.evaluate(ds_test)

print(f'\n\nTest Loss {test_loss}, Test Accuracy {test_accuracy}')
