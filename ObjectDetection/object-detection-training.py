import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as npimg
import os
import pandas as pd

# ## Keras
import keras
import tensorflow as tf

from keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import Convolution2D, MaxPooling2D, Dropout, Flatten, Dense

#
# import cv2
# import pandas as pd
# import random
# import ntpath
#
# ## Sklearn
# from sklearn.utils import shuffle
# from sklearn.model_selection import train_test_split
# import matplotlib


columns = ['Image Path', 'Label']
num_bins = 25
samples_per_bin = 200


# Function to load the dataset from the CSV files
def load_dataset(dirs):
    data = []
    for directory in dirs:
        csv_path = os.path.join(directory, 'captured_data.csv')
        df = pd.read_csv(csv_path)
        data.append(df)
    return pd.concat(data, ignore_index=True)


# Hyperparameters
input_shape = (224, 224, 3)  # Modify the input shape based on your chosen pre-trained model
num_classes = 1  # Number of object classes, change accordingly
root_directory='D:\Master\ProjectOutsideOfCouseScope\ObjectDetection\ '
# Load the dataset
dirs = [
    'D:\Master\ProjectOutsideOfCouseScope\ObjectDetection\captures_20230730_233758',
    'D:\Master\ProjectOutsideOfCouseScope\ObjectDetection\captures_20230731_225555',
    'D:\Master\ProjectOutsideOfCouseScope\ObjectDetection\captures_20230731_225500',
    'D:\Master\ProjectOutsideOfCouseScope\ObjectDetection\captures_20230731_223453',
    'D:\Master\ProjectOutsideOfCouseScope\ObjectDetection\captures_20230731_223329',
    'D:\Master\ProjectOutsideOfCouseScope\ObjectDetection\captures_20230731_223213',
    'D:\Master\ProjectOutsideOfCouseScope\ObjectDetection\captures_20230731_223107',
    'D:\Master\ProjectOutsideOfCouseScope\ObjectDetection\captures_20230731_222917',
    'D:\Master\ProjectOutsideOfCouseScope\ObjectDetection\captures_20230731_222800',
    'D:\Master\ProjectOutsideOfCouseScope\ObjectDetection\captures_20230731_222634',
    'D:\Master\ProjectOutsideOfCouseScope\ObjectDetection\captures_20230731_194859',
]
dataset = load_dataset(dirs)

print(dataset)

# Split dataset into train and test sets (you can also use validation set)
train_split = 0.8
train_size = int(train_split * len(dataset))
train_df = dataset[:train_size]
test_df = dataset[train_size:]
