import logging
import os
from logging.handlers import TimedRotatingFileHandler
from time import strftime

import nlp2
from flask import Flask, request, Response
from flask_caching import Cache
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
import json
from nlp2go.util import NumpyEncoder

logger = logging.getLogger(__name__)
cache = Cache(config={'CACHE_TYPE': 'simple'})


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

    def make_app(self, models, model_detail) -> Flask:
        app = Flask(__name__)
        cache.init_app(app)

        def make_cache_key():
            return str(request.json) + str(request.full_path)

        @app.route('/api/<path>', methods=['POST'])
        @cache.cached(timeout=3600, key_prefix=make_cache_key)
        def predict(path) -> Response:
            print("api request", path, request.json)
            if path in models:
                pred_json = {}
                for k, v in request.json.items():
                    pred_json[k + "_component"] = v
                result_dict = models[path].predict(pred_json)
                response_json = json.dumps(result_dict, ensure_ascii=False, cls=NumpyEncoder,
                                           indent=4,
                                           sort_keys=True)
                return Response(response_json)
            else:
                raise self.ServerError("parameter not found", 404)

        @app.route('/api/config', methods=['GET'])
        def config() -> Response:
            try:
                response_json = json.dumps(model_detail, ensure_ascii=False, cls=NumpyEncoder,
                                           indent=4,
                                           sort_keys=True)
                return Response(response_json)
            except:
                raise self.ServerError("parameter not found", 404)

        @app.after_request
        def after_request(response):
            timestamp = strftime('[%Y-%b-%d %H:%M]')
            response_json = json.loads(response.get_data())
            if response_json is not None and 'result' in response_json:
                logger.error('%s %s %s %s', timestamp, request.access_route, request.json,
                             response_json['result'])
            return response

        return app

    def start(self, models, port, model_detail_dict):
        log_dir = nlp2.get_dir_with_notexist_create('./log/')
        handler = TimedRotatingFileHandler(os.path.join(log_dir, 'api.log'), when="midnight", interval=1)
        handler.suffix = "%Y%m%d"
        logger.setLevel(logging.ERROR)
        logger.addHandler(handler)

        print("hosting api in path: /api/+", list(models.keys()))
        app = self.make_app(models, model_detail_dict)
        CORS(app)

        http_server = WSGIServer(('0.0.0.0', port), app)
        print(f"Model loaded, serving demo on port {port}")
        http_server.serve_forever()
