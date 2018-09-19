from tensorflow.keras.models import Model, load_model
import tensorflowjs as tfjs
from optparse import OptionParser
import os

def extract_realtime_model(full_model):
    input = full_model.get_layer('input').input
    output = full_model.get_layer('output_realtime').output
    model = Model(inputs=input, outputs=output)
    return model

def main(model_path, output_path):
    model = load_model(model_path)
    realtime_model = extract_realtime_model(model)
    realtime_model.compile(optimizer=model.optimizer, loss=model.loss)
    tfjs.converters.save_keras_model(realtime_model, output_path)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-m', '--model_path', dest='model_path',
            default=os.path.join(os.path.dirname(__file__),
                'models/model.h5'),
            help='path to the input model YAML file', metavar='MODEL_PATH')
    parser.add_option('-o', '--output_path', dest='output_path',
            default=os.path.join(os.path.dirname(__file__),
                'static/model'),
            help='path to the output TFJS model directory',
            metavar='OUTPUT_PATH')
    options, args = parser.parse_args()

    main(options.model_path, options.output_path)
