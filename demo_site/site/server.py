import argparse
import os
import sys
from http.client import HTTPException

import requests
from gevent.pywsgi import WSGIServer
from flask import Flask, request, send_from_directory, send_file, jsonify, Response
from flask_cors import CORS


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


def make_app(static_dir: str = None) -> Flask:
    static_dir = os.path.abspath(static_dir)
    app = Flask(__name__, static_folder=static_dir)
    api_url = os.environ["REACT_APP_API_URL"]

    @app.route('/')
    def index() -> Response:  # pylint: disable=unused-variable
        if static_dir is not None:
            return send_file(os.path.join(static_dir, 'index.html'))

    @app.route('/<path:path>')
    def static_proxy(path: str) -> Response:
        if static_dir is not None:
            return send_from_directory(static_dir, path)
        else:
            return send_file(os.path.join(static_dir, 'index.html'))

    @app.route('/api', methods=['POST'])
    def api():
        content = request.json
        task_id = request.args.get("id")
        response = requests.post(url=api_url + task_id, json=content)
        return jsonify(response.json())

    @app.route('/config', methods=['GET'])
    def config():
        response = requests.get(url=api_url + 'config')
        return jsonify(response.json())

    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify(error=str(e)), code

    return app


def main(args):
    parser = argparse.ArgumentParser(description='Serve up a simple model')
    parser.add_argument('--static-dir', default='./public', type=str, help='serve index.html from this directory')
    parser.add_argument('--port', type=int, default=80, help='port to serve the demo on')

    args = parser.parse_args(args)
    app = make_app(static_dir=args.static_dir)
    CORS(app)

    http_server = WSGIServer(('0.0.0.0', args.port), app)
    http_server.serve_forever()


if __name__ == "__main__":
    main(sys.argv[1:])
