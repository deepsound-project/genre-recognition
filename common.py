import numpy as np
import librosa as lbr
import tensorflow.keras.backend as K

GENRES = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal',
        'pop', 'reggae', 'rock']
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
    f = K.function([input, K.learning_phase()], [output])
    return lambda x: f([x, 0])[0] # learning_phase = 0 means test

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
