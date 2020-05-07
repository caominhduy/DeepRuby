# DeepRuby
A rubik solver that uses machine learning and she will be smart (not yet!)

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![License](http://img.shields.io/:license-mit-blue.svg)](https://github.com/caominhduy/DeepRuby/blob/master/LICENSE.txt)

## Disclaimer
1. DeepRuby is written in Mac environment with Python 3.7.1 and TensorFlow 2.1.0 installed, acceptance tests for others have not been done.
2. This project is still in development, the accuracy at the moment may not satisfy your expectation. All pull requests and comments are very welcomed!

## Getting Started
Here you will find the answers to the questions What, Which, Why, and How to install this project on your local machine (and avoid unnecessary panic and scream.)

### About This Project
Rubik cube was created in 1970, yet still, it has been one of the most famous logical toys since then. Every cube has many different permutations or so-called different states. The number of these varies by the types of cube: whereas a 2x2x2 rubik cube has 3,674,160 different states, the 3x3x3 has up to 43,252,003,274,489,856,000 permutations!

Theoretically, one can solve a rubik cube easily by generating all possible permutations into a tree before passing it to the pathfinding algorithms. In reality, however, when the dimension expands, this solution becomes more impossible due to limited memory and processing power. So, if one can generate a small (not too small, though) input of random permutations from the start state, pass it into a deep neural network and let the system learn from it to find the relationship between different features such that it can solve all other permutations, the problem is solved!
### Prerequisites
The package requires `tensorflow`, `numpy`, and `pandas`.

To install:
  * [TensorFlow](https://www.tensorflow.org/install/pip)
  * [NumPy](https://scipy.org/install.html)
  * [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)

### Installing
To clone the latest version of this project
```
git clone https://github.com/caominhduy/DeepRuby/
```

### Repository Structure
```
DeepRuby/
|
|- datasets/
|   |- test/
|   |- train/
|
|- recycle/
|
|- basics.py
|- dependencies.py
|- LICENSE.txt
|- README.md
|- tensor.py
|- test_dataset.py
└─ train_dataset.py
```
1. `datasets` stores the training and validating (testing) datasets. They can be deleted and automatically re-created by calling `test_dataset.py` or `train_dataset.py`.

2. Under `test` or `train` may be subfolders with integer-labeled names. These are made after the rubik type, i.e. 2x2x2 rubik training dataset is stored in `datasets\train\2`.

3. `basics.py`, `dependencies.py`, `tensor.py`, `test_dataset.py`, and `train_dataset.py` are required modules and their paths must not be modified.
  * `basics.py` has basic functions and mechanics to frame the rubik cube.
  * `dependencies.py` has few important functions.
  * `test_dataset.py` and `train_dataset.py` are run to generate datasets for training and validating (their details are discussed later).
  * `tensor.py` does all the training and testing.


4. `recycle` is a graveyard of dead modules and dead codes. Let's not wasting our time reading them (well, you read it, but then I will feel guilty for not explaining, so I mean **"our time"**).

## Understanding
In this part, we discuss the scripts in details.
### **`basics.py`**
This file works as the frame of the project. _(And it is surprisingly tedious!)_

* `RUBIK_SIZE` **decides the dimension of rubik cube** _(i.e. 3x3x3 rubik cube is 3)_. It is **the most important constant** since it is very universal. You can change this constant to change the behavior of entire packet.
* `init_cube` takes **RUBIK_SIZE** and creates an complete (solved) rubik cube as an array of 6 multidimensional numpy array (each one is equivalent to a side of a rubik cube)
  - For example: a rubik 3x3x3 should look like this

  |   |   |   | b | b | b |   |   |   |   |   |   |
  |---|---|---|---|---|---|---|---|---|---|---|---|
  |   |   |   | b | b | b |   |   |   |   |   |   |
  |   |   |   | b | b | b |   |   |   |   |   |   |
  | o | o | o | w | w | w | r | r | r | y | y | y |
  | o | o | o | w | w | w | r | r | r | y | y | y |
  | o | o | o | w | w | w | r | r | r | y | y | y |
  |   |   |   | g | g | g |   |   |   |   |   |   |
  |   |   |   | g | g | g |   |   |   |   |   |   |
  |   |   |   | g | g | g |   |   |   |   |   |   |

_GitHub Markdown forces the first row to be header, so please ignore the boldness of the top 3 blues_

* `turn` takes 2 arguments: one available rotation and current rubik cube multidimensional array. It returns the new state after rotation.
  - This is the most tedious part in this repo.
  - **Reversed notations** and **repeated notations** are just 6 basic notations after 3 & 2 basic rotations, subsequently.
  - In real life, the rubik professionals (in competitions) may have more moves than these 18 basic moves, those are technically the same but only faster.
  - These 18 notations, human-friendly, are written as:
  | U, L, R, D, F, B  | U', L', R', D', F', B'  |  U2, L2, R2, D2, F2, B2 |
  |---|---|---|
  |  Rotating specific side 90º clockwisely   |  Rotating specific side 90º **counterclockwisely**  |Rotating specific side 180º |

* `rotating_notations` decides the values for the last column in the datasets (addressed later).

### **`dependencies.py`**
This module contains slighty less important functions.
* `rubik_to_array` takes a **rubik** and a `RUBIK_SIZE`, flatten down to a single 1-D array.

* `array_to_rubik` reverses it, but it is currently no longer in used.


* `get_latest_file` lists all the file under specified directory, and returns path to the csv dataset file with largest number (for reason why largest number please see module `test_dataset.py`.)

### **`test_dataset.py`**
This module generates dataset for testing. Many functions are also applicable for `training_dataset.py`.

* `TEST_DATASET_SIZE` decides the dataset size (number of different states). The final dataset may be smaller than this value due to `duplicate_removal` or `duplicate_removal_v2`.


* `datetime_` returns a string of current system time under format YYMMDDHrHrMinMin (in 24-hour format). This simplify the naming process because the lastest dataset now will always have largest number as its name and will be in use for training. (You can take advantage of this by renaming a dataset to time in the future or "9999999999.csv" for example for it to be used instantly for training.)


* `touch` consumes 3 parameters: **dataset type** (i.e. 'test' or 'train'), **RUBIK_SIZE**, and **csv filename**. It constructs the directories (if there haven't), and the dataset file to be written.


* `duplicate_removal` and `duplicate_removal_v2` remove duplicates from dataset: especially in validating process, **repeated values cannot have different result but they change the accuracy**, thus they may poison the dataset's efficiency and accuracy.


* `duplicate_removal_v2` is basically like its original version, but instead of checking the whole line in dataset, it checks for color codes only. In theory, any permutation can have up to 6 `previous_move`, but only one of them should lead it closer to the origin.

* `generator` takes similar parameters as touch, generates new states by doing random rotations and writing them into the new dataset.

The row in dataset looks something like this:

### **`train_dataset.py`**
This module is very similar to previous module. Review `test_dataset.py` if needed.

### **`tensor.py`**
* `COLORS_DICT` is used for integer encoding of colors.


* `ROTATIONAL_DICT` is used for integer encoding of `previous_move`.


* `df_train` and `df_test` are Pandas dataframes for training and testing. They are integer-encoded, shuffle.


* `y_train` and `y_test` are the last column in the dataset (used for labelling dataset in the pipeline to tensor, see `read_dataset_from_dataframe`.)

![Screen-Shot-2020-05-07-at-8-32-41-AM](https://i.ibb.co/Nnbz6D4/Screen-Shot-2020-05-07-at-8-32-41-AM.png)

_At this point, the training provides only approximately 10% of accuracy on test dataset. Improvements are on-the-way._

## Running
1. Modify `RUBIK_SIZE` in `basics.py`
```
RUBIK_SIZE = 2 # example rubik 2x2x2
```
2. Run `test_dataset.py` or `train_dataset.py` (modify `TEST_DATASET_SIZE` and `TRAIN_DATASET_SIZE` before running if needed) to generate new dataset for training and testing (if necessary)
```
python3 test_dataset.py
python3 train_dataset.py
```
3. Build the model
```
python3 tensor.py
```

## Versioning
For the versions available, see module's `__version__`.

## Author
* **Duy Cao** - [caominhduy](https://github.com/caominhduy/)

## Credits
* Special thanks to TensorFlow's Official Tutorial and API Documentation.

## License
This project is licensed under the MIT License - see the LICENSE.txt file for more details

## Machine Learning in-a-nutshell
![How Machines Learn – CGP Grey](https://i.ibb.co/HGScMfv/IMG-5205.png)
[This video by CGP Grey on Youtube](https://youtu.be/6g4O5UOH304) is very fun, straightforward and informative (especially for those who are new or those who are trying to explain to someone who are new.)
