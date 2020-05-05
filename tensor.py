"""
Let's do some training! Credits:
    - Some of the codes were modified from TensorFlow's Tutorial Documentation
"""

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
import pandas as pd

__author__ = 'Duy Cao'
__version__ = '2020.5.5'

start = time()

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
categorical_columns = column_names[:len(column_names)-1]

def get_vocab_list(): # get a dictionary of column name as key and color as item
    colors = ['b', 'o', 'w', 'r', 'y', 'g']
    dict = {}
    for name in column_names[:len(column_names)-1]:
        dict[name] = colors
    return dict

vocab_list = get_vocab_list()

# Load datasets as pandas dataframe

df_train = pd.read_csv( #training dataframe
    train_dataset_path,
    header=None,
    names = column_names,
    skip_blank_lines=True
    )
y_train = df_train.pop('previous_move')

df_test = pd.read_csv( #testing df
    test_dataset_path,
    header=None,
    names = column_names,
    skip_blank_lines=True
    )
y_test = df_test.pop('previous_move')
#print(df_train.head()) # quick read 5 first lines in df
#print(df_train.loc[0], y_train.loc[0]) # the first line

tile_position = []
for tile in categorical_columns:
     # Need to one-hot encode categorical features.
    vocab = df_train[tile].unique()
    tile_position.append(tf.feature_column.categorical_column_with_vocabulary_list(tile, vocab))

def make_input_fn(df_data, df_label, shuffle=True, n_epochs=10,\
                     shuffle_buffer_size=1000, batch_size=200):
    def input_functions():
        ds = tf.data.Dataset.from_tensor_slices((dict(df_data), df_label))
        if shuffle:
            ds = ds.shuffle(shuffle_buffer_size)
        ds = ds.batch(batch_size).repeat(n_epochs)
        return ds # return a BATCH of the dataset
    return input_functions # return a function object for use

train_input_fn = make_input_fn(df_train, y_train) # pass fuction as an object
test_input_fn = make_input_fn(df_test, y_test, shuffle=False, n_epochs=1)

linear_est = tf.estimator.LinearClassifier(feature_columns=tile_position)

linear_est.train(train_input_fn)
#result = linear_est.evaluate(test_input_fn)

#print(result['accuracy'])

if __name__ == "__main__":
    #print("Train dataset")
    #show_batch(train_data)
    #print("\nCategorical columns")
    #print(categorical_columns)
    #print(list(train_data.take(1)))
    print(str(round((time() - start), 3)))

"""
# Load dataset from csv
# very confusing compared to pandas dataframe

# Load datasets
def get_dataset(file_path):
    dataset = tf.data.experimental.make_csv_dataset(
        file_path,
        batch_size = 10,
        column_names=columns,
        label_name='previous_move',
        header=False,
        num_epochs=1,
        shuffle=True,
        shuffle_buffer_size=1000,
        num_rows_for_inference=None,
        ignore_errors=False)
    return dataset

train_data = get_dataset(train_dataset_path)
test_data = get_dataset(test_dataset_path)

categorical_columns = []
for feature, vocab in vocab_list.items():
    cat_col = tf.feature_column.categorical_column_with_vocabulary_list(
        key=feature, vocabulary_list=vocab, default_value=-1)
    categorical_columns.append(tf.feature_column.indicator_column(cat_col))

categorical_layer = tf.keras.layers.DenseFeatures(categorical_columns)


model = tf.keras.Sequential([
    categorical_layer
])

model.compile(
    loss=tf.keras.losses.CategoricalCrossentropy(),
    optimizer='adam',
    metrics=['accuracy'])

model.fit(train_data, epochs=20)


def show_batch(dataset):
  for batch, label in dataset.take(1):
    for key, value in batch.items():
      print("{:20s}: {}".format(key,value.numpy()))
"""
