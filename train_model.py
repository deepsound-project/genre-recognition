from common import GENRES
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Input, Dense, Lambda, Dropout, Activation, LSTM, \
        TimeDistributed, Convolution1D, MaxPooling1D
from sklearn.model_selection import train_test_split
import numpy as np
import pickle
from optparse import OptionParser
from sys import stderr, argv
import os

SEED = 42
N_LAYERS = 3
FILTER_LENGTH = 5
CONV_FILTER_COUNT = 256
LSTM_COUNT = 256
BATCH_SIZE = 32
EPOCH_COUNT = 100

def train_model(data):
    x = data['x']
    y = data['y']
    (x_train, x_val, y_train, y_val) = train_test_split(x, y, test_size=0.3,
            random_state=SEED)

    print('Building model...')

    n_features = x_train.shape[2]
    input_shape = (None, n_features)
    model_input = Input(input_shape, name='input')
    layer = model_input
    for i in range(N_LAYERS):
        # convolutional layer names are used by extract_filters.py
        layer = Convolution1D(
                filters=CONV_FILTER_COUNT,
                kernel_size=FILTER_LENGTH,
                name='convolution_' + str(i + 1)
            )(layer)
        layer = Activation('relu')(layer)
        layer = MaxPooling1D(2)(layer)

    layer = Dropout(0.5)(layer)
    layer = LSTM(LSTM_COUNT, return_sequences=True)(layer)
    layer = Dropout(0.5)(layer)
    layer = TimeDistributed(Dense(len(GENRES)))(layer)
    layer = Activation('softmax', name='output_realtime')(layer)
    time_distributed_merge_layer = Lambda(
            function=lambda x: K.mean(x, axis=1), 
            output_shape=lambda shape: (shape[0],) + shape[2:],
            name='output_merged'
        )
    model_output = time_distributed_merge_layer(layer)
    model = Model(model_input, model_output)
    opt = RMSprop(lr=0.00001)
    model.compile(
            loss='categorical_crossentropy',
            optimizer=opt,
            metrics=['accuracy']
        )

    print('Training...')
    model.fit(x_train, y_train, batch_size=BATCH_SIZE, nb_epoch=EPOCH_COUNT,
              validation_data=(x_val, y_val), verbose=1)

    return model

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-d', '--data_path', dest='data_path',
            default=os.path.join(os.path.dirname(__file__),
                'data/data.pkl'),
            help='path to the data pickle', metavar='DATA_PATH')
    parser.add_option('-m', '--model_path', dest='model_path',
            default=os.path.join(os.path.dirname(__file__),
                'models/model.h5'),
            help='path to the output model HDF5 file', metavar='MODEL_PATH')
    options, args = parser.parse_args()

    with open(options.data_path, 'rb') as f:
        data = pickle.load(f)

    model = train_model(data)

    with open(options.model_path, 'w') as f:
        f.write(model.to_yaml())
    model.save_weights(options.weights_path)
