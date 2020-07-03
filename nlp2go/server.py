import logging
from flask import Flask, request, Response
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
import json
from .util import NumpyEncoder

logger = logging.getLogger(__name__)


class Server:
    class ServerError(Exception):
        status_code = 400

        def __init__(self, message, status_code=None, payload=None):
            Exception.__init__(self)
            self.message = message
            if status_code is not None:
                self.status_code = status_code
            self.payload = payload

        def to_dict(self):
            error_dict = dict(self.payload or ())
            error_dict['message'] = self.message
            return error_dict

    def make_app(self, models) -> Flask:
        app = Flask(__name__)  # pylint: disable=invalid-name

        @app.route('/api/<path>', methods=['GET', 'POST'])
        def predict(path) -> Response:
            if path in models:
                result_dict = models[path].predict(dict(request.values), enable_input_panel=False)
                return json.dumps({'result': result_dict['result']}, ensure_ascii=False, cls=NumpyEncoder,
                                  indent=4,
                                  sort_keys=True)
            else:
                raise self.ServerError("parameter not found", 404)

        return app

    def start(self, models, port):
        print("hosting api in path: /api/+", list(models.keys()))
        app = self.make_app(models)
        CORS(app)

        http_server = WSGIServer(('0.0.0.0', port), app)
        print(f"Model loaded, serving demo on port {port}")
        http_server.serve_forever()
