from common import get_layer_output_function, WINDOW_SIZE, WINDOW_STRIDE
from tensorflow.keras.models import model_from_yaml
import librosa as lbr
import numpy as np
from functools import partial
from optparse import OptionParser
import cPickle
import os

def compose(f, g):
    return lambda x: f(g(x))

def undo_layer(length, stride, (i, j)):
    return (stride * i, stride * (j - 1) + length)

def extract_filters(model, data, filters_path, count0):
    x = data['x']
    track_paths = data['track_paths']

    conv_layer_names = []
    i = 1
    while True:
        name = 'convolution_' + str(i)
        if model.get_layer(name) is None:
            break
        conv_layer_names.append(name)
        i += 1

    # Generate undoers for every convolutional layer. Undoer is a function
    # translating a pair of coordinates in feature space (mel spectrograms or
    # features extracted by convolutional layers) to the sample space (raw
    # audio signal).
    conv_layer_undoers = []

    # undo the mel spectrogram extraction
    undoer = partial(undo_layer, WINDOW_SIZE, WINDOW_STRIDE)

    for name in conv_layer_names:
        layer = model.get_layer(name)
        length = layer.filter_length
        stride = layer.subsample_length

        # undo the convolution layer
        undoer = compose(partial(undo_layer, length, stride), undoer)
        conv_layer_undoers.append(undoer)

        # undo the pooling layer
        undoer = compose(partial(undo_layer, 2, 2), undoer)
        conv_layer_output_funs = \
        map(partial(get_layer_output_function, model), conv_layer_names)

    # Extract track chunks with highest activations for each filter in each
    # convolutional layer.
    for (layer_index, output_fun) in enumerate(conv_layer_output_funs):
        layer_path = os.path.join(filters_path, conv_layer_names[layer_index])
        if not os.path.exists(layer_path):
            os.makedirs(layer_path)

        print('Computing outputs for layer', conv_layer_names[layer_index])
        output = output_fun(x)

        # matrices of shape n_tracks x time x n_filters
        max_over_time = np.amax(output, axis=1)
        argmax_over_time = np.argmax(output, axis=1)

        # number of input chunks to extract for each filter
        count = count0 // 2 ** layer_index
        argmax_over_track = \
                np.argpartition(max_over_time, -count, axis=0)[-count :, :]

        undoer = conv_layer_undoers[layer_index]

        for filter_index in range(argmax_over_track.shape[1]):
            print('Processing layer', conv_layer_names[layer_index], \
                    'filter', filter_index)
            
            track_indices = argmax_over_track[:, filter_index]
            time_indices = argmax_over_time[track_indices, filter_index]
            sample_rate = [None]

            def extract_sample_from_track(undoer, (track_index, time_index)):
                track_path = track_paths[track_index]    
                (track_samples, sample_rate[0]) = lbr.load(track_path,
                        mono=True)
                (t1, t2) = undoer((time_index, time_index + 1))
                return track_samples[t1 : t2]

            samples_for_filter = np.concatenate(
                    map(partial(extract_sample_from_track, undoer),
                            zip(track_indices, time_indices)))

            filter_path = os.path.join(layer_path,
                    '{}.wav'.format(filter_index))
            lbr.output.write_wav(filter_path, samples_for_filter,
                    sample_rate[0])

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-m', '--model_path', dest='model_path',
            default=os.path.join(os.path.dirname(__file__),
                'models/model.yaml'),
            help='path to the model YAML file', metavar='MODEL_PATH')
    parser.add_option('-w', '--weights_path', dest='weights_path',
            default=os.path.join(os.path.dirname(__file__),
                'models/weights.h5'),
            help='path to the model weights hdf5 file',
            metavar='WEIGHTS_PATH')
    parser.add_option('-d', '--data_path', dest='data_path',
            default=os.path.join(os.path.dirname(__file__),
                'data/data.pkl'),
            help='path to the data pickle',
            metavar='DATA_PATH')
    parser.add_option('-f', '--filters_path', dest='filters_path',
            default=os.path.join(os.path.dirname(__file__),
                'filters'),
            help='path to the output filters directory',
            metavar='FILTERS_PATH')
    parser.add_option('-c', '--count0', dest='count0',
            default='4',
            help=('number of chunks to extract from the first convolutional ' +
                'layer, this number is halved for each next layer'),
            metavar='COUNT0')
    options, args = parser.parse_args()

    with open(options.model_path, 'r') as f:
        model = model_from_yaml(f.read())
    model.load_weights(options.weights_path)

    with open(options.data_path, 'r') as f:
        data = cPickle.load(f)

    extract_filters(model, data, options.filters_path, int(options.count0))
