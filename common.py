# To avoid errors during importing librosa.
import matplotlib
matplotlib.use('Agg')

import numpy as np
import librosa as lbr
import keras.backend as K

GENRES = ['international', 'blues', 'jazz', 'classical', 'old-time/historic', 'country', 'pop',
        'rock', 'easy listening', 'soul/rnb', 'electronic', 'folk' ,'spoken', 'hip-hop', 'experimental', 'instrumental']

GENRE_IDS = [2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 14, 15, 17, 20, 21, 38, 1235]
GENRE_IDS_STRS = ["2.0", "3.0", "4.0", "5.0", "6.0", "8.0", "9.0", "10.0", "12.0", "13.0", "14.0", "15.0", "17.0", "20.0", "21.0", "38.0", "1235.0"]

NUMTRACKS = [5271, 1752, 4126, 4106, 868, 1987, 13845, 32923, 730, 1499, 34413, 12706, 1876, 8389, 38154, 14938]

WINDOW_SIZE = 2048
WINDOW_STRIDE = WINDOW_SIZE // 2
N_MELS = 128

MEL_KWARGS = {
    'n_fft': WINDOW_SIZE,
    'hop_length': WINDOW_STRIDE,
    'n_mels': N_MELS
}

def get_layer_output_function(model, layer_name):
    input = model.get_layer('input').input
    output = model.get_layer(layer_name).output
    f = K.function([input, K.learning_phase()], output)
    return lambda x: f([x, 0]) # learning_phase = 0 means test

def load_track(filename, enforce_shape=None):
    
    new_input, sample_rate = lbr.load(filename, mono=True)
    features = lbr.feature.melspectrogram(new_input, **MEL_KWARGS).T

    if enforce_shape is not None:
        if features.shape[0] < enforce_shape[0]:
            delta_shape = (enforce_shape[0] - features.shape[0],
                    enforce_shape[1])
            features = np.append(features, np.zeros(delta_shape), axis=0)
        elif features.shape[0] > enforce_shape[0]:
            features = features[: enforce_shape[0], :]

    features[features == 0] = 1e-6
    return (np.log(features), float(new_input.shape[0]) / sample_rate)
