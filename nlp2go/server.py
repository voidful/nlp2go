import argparse
import logging
from collections import defaultdict

from flask import Flask, request, Response
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
import json
import numpy as np
from .model import Model

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


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


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """

    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32,
                              np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):  #### This is the fix
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def make_app() -> Flask:
    global model_dict
    app = Flask(__name__)  # pylint: disable=invalid-name

    @app.route('/<path>', methods=['POST'])
    def predict(path) -> Response:
        if "input" in request.values and path in model_dict:
            input = request.values["input"]
            result = model_dict[path]['model'].predict(input, model_dict[path].get('predictor', 'just'))
            return json.dumps(result, ensure_ascii=False, cls=NumpyEncoder)
        else:
            raise ServerError("parameter not found", 404)

    return app


def main():
    global model_dict
    model_dict = defaultdict(dict)
    parser = argparse.ArgumentParser(description='Serve up a simple model')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--json', type=str)
    group.add_argument('--model', type=str)
    parser.add_argument('--predictor', type=str, choices=['tag', 'biotag'])
    parser.add_argument('--path', type=str, default="API", help='api path to serve the demo')
    parser.add_argument('--port', type=int, default=3010, help='port to serve the demo on')
    args = parser.parse_args()

    if args.model:
        model = Model()
        model.load_model(args.model)
        model_detail = {'model': model, 'predictor': args.predictor}
        model_dict[args.path].update(model_detail)

        model2 = Model()
        model2.load_model(args.model)
        model_detail2 = {'model': model, 'predictor': 'tag'}
        model_dict[args.path + "2"].update(model_detail2)

    print("hosting api in path: ", list(model_dict.keys()))
    app = make_app()
    CORS(app)

    http_server = WSGIServer(('0.0.0.0', args.port), app)
    print(f"Model loaded, serving demo on port {args.port}")
    http_server.serve_forever()


if __name__ == "__main__":
    main()
