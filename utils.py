import os

import markovify
from keras.layers import LSTM
from keras.models import Sequential

from documented_model import ARTIST_NAME, TRAIN_MODE


def create_network(depth):
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
    model.compile(optimizer='rmsprop',
                  loss='mse')

    if ARTIST_NAME + ".rap" in os.listdir(".") and TRAIN_MODE == False:
        # loads the weights from the hdf5 file saved earlier
        model.load_weights(str(ARTIST_NAME + ".rap"))
        print("loading saved network: " + str(ARTIST_NAME) + ".rap")
    return model


def create_markov_model(text_file):
    read = open(text_file, "r").read()
    # markovify goes line by line of the lyrics.txt file and
    # creates a model of the text which allows us to use
    # make_sentence() later on to create a bar for lyrics
    # creates a probability distribution for all the words
    # so it can generate words based on the current word we're on
    text_model = markovify.NewlineText(read)
    return text_model
