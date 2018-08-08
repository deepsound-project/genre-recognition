from genre_recognizer import GenreRecognizer
from common import GENRES
import numpy as np
import os
import json
import uuid
from random import random
import time
import tornado
import tornado.ioloop
import tornado.web
from optparse import OptionParser

STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')
UPLOADS_PATH = os.path.join(os.path.dirname(__file__), 'uploads')

genre_recognizer = None

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render(os.path.join(STATIC_PATH, 'index.html'))

class PlayHandler(tornado.web.RequestHandler):

    def get(self):
        self.render(os.path.join(STATIC_PATH, 'play.html'))

class UploadHandler(tornado.web.RequestHandler):

    def post(self):
        file_info = self.request.files['filearg'][0]
        file_name = file_info['filename']
        file_extension = os.path.splitext(file_name)[1]
        file_uuid = str(uuid.uuid4())
        uploaded_name = file_uuid + file_extension

        if not os.path.exists(UPLOADS_PATH):
            os.makedirs(UPLOADS_PATH)

        uploaded_path = os.path.join(UPLOADS_PATH, uploaded_name)
        with open(uploaded_path, 'wb') as f:
            f.write(file_info['body'])
        (predictions, duration) = genre_recognizer.recognize(
                uploaded_path)
        genre_distributions = self.get_genre_distribution_over_time(
                predictions, duration)
        json_path = os.path.join(UPLOADS_PATH, file_uuid + '.json')
        with open(json_path, 'w') as f:
            f.write(json.dumps(genre_distributions))
        self.finish('"{}"'.format(file_uuid))

    def get_genre_distribution_over_time(self, predictions, duration):
        '''
        Turns the matrix of predictions given by a model into a dict mapping
        time in the song to a music genre distribution.
        '''
        predictions = np.reshape(predictions, predictions.shape[1:])
        n_steps = predictions.shape[0]
        delta_t = duration / n_steps

        def get_genre_distribution(step):
            return {genre_name: float(predictions[step, genre_index])
                    for (genre_index, genre_name) in enumerate(GENRES)}

        return [((step + 1) * delta_t, get_genre_distribution(step))
                for step in range(n_steps)]

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/play.html', PlayHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {
        'path': STATIC_PATH
    }),
    (r'/uploads/(.*)', tornado.web.StaticFileHandler, {
        'path': UPLOADS_PATH
    }),
    (r'/upload', UploadHandler),
], debug=True)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-m', '--model', dest='model_path',
            default=os.path.join(os.path.dirname(__file__), 
                'models/model.h5'),
            help='load keras model from MODEL yaml file', metavar='MODEL')
    parser.add_option('-p', '--port', dest='port',
            default=8080,
            help='run server at PORT', metavar='PORT')
    options, args = parser.parse_args()
    genre_recognizer = GenreRecognizer(options.model_path)
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
