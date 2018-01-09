'''
GPU command:
THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python train_model.py
'''

from common import GENRES
from keras.callbacks import Callback
from keras.utils import np_utils
from keras.models import Model
from keras.optimizers import RMSprop,Adam
from keras import backend as K
from keras.layers import Input, Dense, Lambda, Dropout, Activation, LSTM, \
        TimeDistributed, Convolution1D, MaxPooling1D,Conv1D,AveragePooling1D, Flatten,GlobalAveragePooling1D,GlobalMaxPooling1D,concatenate
from sklearn.model_selection import train_test_split
import numpy as np
import cPickle
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

    print 'Building model...'

    n_features = x_train.shape[2]
    input_shape = (None, n_features)
    model_input = Input(input_shape, name='input')
    layer = model_input
    for i in range(N_LAYERS):
        # convolutional layer names are used by extract_filters.py
        layer = Convolution1D(
                nb_filter=CONV_FILTER_COUNT,
                filter_length=FILTER_LENGTH,
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

    print 'Training...'
    model.fit(x_train, y_train, batch_size=BATCH_SIZE, nb_epoch=EPOCH_COUNT,
              validation_data=(x_val, y_val), verbose=1)

    return model

def train_model_spotify(data):
    '''Model implemented for genre recognition by Nikhil George Titus based on http://benanne.github.io/2014/08/05/spotify-cnns.html'''
    x = data['x']
    y = data['y']
    (x_train, x_val, y_train, y_val) = train_test_split(x, y,stratify=y, test_size=0.2,random_state=SEED)

    print 'Building model...'

    input_shape = (x_train.shape[1], x_train.shape[2])
    print input_shape
    model_input = Input(shape=input_shape)
    layer = model_input
    for i in range(3):
        layer = Conv1D(filters=256, kernel_size=4,strides=2)(layer)
        layer = Activation('relu')(layer)
        layer = MaxPooling1D(2)(layer)
    averagePool = GlobalAveragePooling1D()(layer)
    maxPool = GlobalMaxPooling1D()(layer)
    layer = concatenate([averagePool, maxPool])
    layer = Dropout(rate=0.5)(layer)
    layer = Dense(units=len(GENRES))(layer)
    model_output = Activation('softmax')(layer)
    model = Model(model_input, model_output)
    opt = Adam()
    model.compile(loss='categorical_crossentropy',optimizer=opt,metrics=['accuracy'])
    model.fit(x_train, y_train,batch_size=BATCH_SIZE,epochs=80,validation_data=(x_val, y_val),verbose=1)
    return model

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-d', '--data_path', dest='data_path',
            default=os.path.join(os.path.dirname(__file__),
                'data/data.pkl'),
            help='path to the data pickle', metavar='DATA_PATH')
    parser.add_option('-m', '--model_path', dest='model_path',
            default=os.path.join(os.path.dirname(__file__),
                'models/model.yaml'),
            help='path to the output model YAML file', metavar='MODEL_PATH')
    parser.add_option('-w', '--weights_path', dest='weights_path',
            default=os.path.join(os.path.dirname(__file__),
                'models/weights.h5'),
            help='path to the output model weights hdf5 file',
            metavar='WEIGHTS_PATH')
    parser.add_option('-c', '--model_choice', dest='model_choice',
            default=1,
            help='Model choice: 1 for LSTM and 2 for fully connected model based on http://benanne.github.io/2014/08/05/spotify-cnns.html',
            metavar='WEIGHTS_PATH')
    options, args = parser.parse_args()

    with open(options.data_path, 'r') as f:
        data = cPickle.load(f)

    if options.model_choice == 1:
        model = train_model(data)
    else:
        model=train_model_spotify(data)

    with open(options.model_path, 'w') as f:
        f.write(model.to_yaml())
    model.save_weights(options.weights_path)
