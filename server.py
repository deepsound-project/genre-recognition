import os
import tornado
import tornado.ioloop
import tornado.web
from optparse import OptionParser

STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')

genre_recognizer = None

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render(os.path.join(STATIC_PATH, 'index.html'))

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {
        'path': STATIC_PATH
    }),
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
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
