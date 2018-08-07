from common import load_track, get_layer_output_function
import numpy as np
from tensorflow.keras.layers import Input
from tensorflow.keras.models import model_from_yaml, Model
from tensorflow.keras import backend as K

class GenreRecognizer():

    def __init__(self, model_path, weights_path):
        with open(model_path, 'r') as f:
            dupa = f.read()
            model = model_from_yaml(dupa)
        model.load_weights(weights_path)
        self.pred_fun = get_layer_output_function(model, 'output_realtime')
        print('Loaded model.')
    
    def recognize(self, track_path):
        print('Loading song', track_path)
        (features, duration) = load_track(track_path)
        features = np.reshape(features, (1,) + features.shape)
        return (self.pred_fun(features), duration)
