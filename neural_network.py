import os

import numpy as np
from keras.layers import LSTM
from keras.models import Sequential

from conf import ARTIST_NAME
from utils import (
    convert_index_of_most_common_rhyme_into_float,
    calculate_count_of_syllables_as_fraction,
)


def create_network(depth, ARTIST_NAME, TRAIN_MODE):
    # Sequential() creates a linear stack of layers
    model = Sequential()
    # Adds a LSTM layer as the first layer in the network with
    # 4 units (nodes), and a 2x2 tensor (which is the same shape as the
    # training data)
    model.add(LSTM(4, input_shape=(2, 2), return_sequences=True))
    # adds 'depth' number of layers to the network with 8 nodes each
    for i in range(depth):
        model.add(LSTM(8, return_sequences=True))
    # adds a final layer with 2 nodes for the output
    model.add(LSTM(2, return_sequences=True))
    # prints a summary representation of the model
    model.summary()
    # configures the learning process for the network / model
    # the optimizer function rmsprop: optimizes the gradient descent
    # the loss function: mse: will use the "mean_squared_error when trying to improve
    model.compile(optimizer="rmsprop", loss="mse")

    if ARTIST_NAME + ".rap" in os.listdir(".") and TRAIN_MODE == False:
        # loads the weights from the hdf5 file saved earlier
        model.load_weights(str(ARTIST_NAME + ".rap"))
        print("loading saved network: " + str(ARTIST_NAME) + ".rap")
    return model


def train(x_data, y_data, model):
    # fit is used to train the model for 5 'epochs' (iterations) where
    # the x_data is the training data, and the y_data is the target data
    # x is the training and y is the target data
    # batch_size is a subset of the training data (2 in this case)
    # verbose simply shows a progress bar
    model.fit(np.array(x_data), np.array(y_data), batch_size=2, epochs=5, verbose=1)
    # save_weights saves the best weights from training to a hdf5 file
    model.save_weights(ARTIST_NAME + ".rap")


def build_dataset(lyrics, rhyme_list):
    dataset = []
    line_list = []
    # line_list becomes a list of the line from the lyrics, the syllables for that line (either 0 or 1 since
    # syllables uses integer division by maxsyllables (16)), and then rhyme returns the most common word
    # endings of the words that could rhyme with the last word of line
    for line in lyrics:
        line_list = [
            line,
            calculate_count_of_syllables_as_fraction(line),
            convert_index_of_most_common_rhyme_into_float(line, rhyme_list),
        ]
        dataset.append(line_list)

    with open("training_data.dataset", "w+") as opened_file:
        for one_data in dataset:
            opened_file.write("{}\n".format(one_data))
    x_data = []
    y_data = []

    # using range(len(dataset)) - 3 because of the way the indices are accessed to
    # get the lines
    for i in range(len(dataset) - 3):
        line1 = dataset[i][1:]
        line2 = dataset[i + 1][1:]
        line3 = dataset[i + 2][1:]
        line4 = dataset[i + 3][1:]

        # populate the training data
        # grabs the syllables and rhyme index here
        x = [line1[0], line1[1], line2[0], line2[1]]
        x = np.array(x)
        # the data is shaped as a 2x2 array where each row is a
        # [syllable, rhyme_index] pair
        x = x.reshape(2, 2)
        x_data.append(x)

        # populate the target data
        y = [line3[0], line3[1], line4[0], line4[1]]
        y = np.array(y)
        y = y.reshape(2, 2)
        y_data.append(y)

    # returns the 2x2 arrays as datasets
    x_data = np.array(x_data)
    y_data = np.array(y_data)

    # print "x shape " + str(x_data.shape)
    # print "y shape " + str(y_data.shape)
    return x_data, y_data
