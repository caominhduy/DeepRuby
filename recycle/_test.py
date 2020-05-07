import numpy as np
import math
from basics import *
from dependencies import *
from tensor import *

# THIS IS THE REMAIN OF A NUCLEAR TEST SITE, DANGEROUS!
# Nah, they are just old and unused codes, but danger is real

coin = np.matrix('1 2 3; 4 5 6; 7 8 9')

coin2 = np.matrix('11 22 33; 44 55 66; 77 88 99')

coin2[:,2] = np.flipud(np.rot90(coin))[:,0]

def get_vocab_list():
    column_names = get_column_name(RUBIK_SIZE)
    colors = ['b', 'o', 'w', 'r', 'y', 'g']
    dict = {}
    for name in column_names[:len(column_names)-1]:
        dict[name] = colors
    return dict

if __name__ == '__main__':
    x = ['b','b','o','o','o','g','o','g','w','w','w','w','b','r','b','r','y','y','y','y','r','r','g','g']
    y = get_vocab_list()
    print(y)

"""
model = tf.keras.Sequential([
  tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(
    loss=tf.keras.losses.CategoricalCrossentropy(),
    optimizer='adam',
    metrics=['accuracy'])

model.fit(ds_train, epochs=1)

print(model.summary())
"""
"""
model.compile(
    loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
    optimizer='adam',
    metrics=['accuracy'])
"""
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


"""
tile_position = []
for tile in categorical_columns:
     # Need to one-hot encode categorical features.
    vocab = df_train[tile].unique()
    tile_position.append(tf.feature_column.categorical_column_with_vocabulary_list(tile, vocab))

print(tile_position)

def make_input_fn(data_df, label_df, num_epochs=10, shuffle=True, batch_size=32):
    def input_function():
        ds = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))
        if shuffle:
          ds = ds.shuffle(1000)
        ds = ds.batch(batch_size).repeat(num_epochs)
        return ds
    return input_function

train_input_fn = make_input_fn(df_train, y_train) # pass fuction as an object
test_input_fn = make_input_fn(df_test, y_test, num_epochs=1, shuffle=False)

linear_est = tf.estimator.LinearClassifier(feature_columns=tile_position)

linear_est.train(train_input_fn) result = linear_est.evaluate(test_input_fn)

#print(result['accuracy'])

if __name__ == "__main__":
    #print("Train dataset")
    #show_batch(train_data)
    #print("\nCategorical columns")
    #print(categorical_columns)
    #print(list(train_data.take(1)))
    print(str(round((time() - start), 3)))
"""
