import argparse
from collections import defaultdict
import json

from nlp2go.cli import Cli
from nlp2go.model import Model
from nlp2go.server import Server

import os

os.environ["PYTHONIOENCODING"] = "utf-8"


def parse_args(args):
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--json', type=str)
    group.add_argument('--model', type=str)
    parser.add_argument('--panel', action='store_true', help='enable panel to input argument')
    # interface
    parser.add_argument('--api_path', type=str, default="model", help='api path to serve the demo')
    parser.add_argument('--api_port', type=int, default=3000, help='port to serve the demo on')
    parser.add_argument('--cli', action='store_true', help='commandline mode')

    input_arg, others_arg = parser.parse_known_args(args)
    input_arg = {k: v for k, v in vars(input_arg).items() if v is not None}
    others_arg = {k.replace("--", ""): v for k, v in zip(others_arg[:-1:2], others_arg[1::2])}
    return input_arg, others_arg


def main(arg=None):
    """
    loading argument and starting an model interface
    """
    global model_dict
    model_dict = defaultdict(dict)
    args, others_arg = parse_args(arg)
    loaded_model = {}
    if args.get('model', None):
        loaded_model[args.get('api_path')] = Model(args.get('model'), args.get('panel', False), **others_arg)
    else:
        with open(args.get('json'), 'r', encoding='utf8') as reader:
            model_dict = json.loads(reader.read())
        for path, d in model_dict.items():
            model = Model(model_dict[path]['model'], args.get('panel', False), **model_dict[path])
            loaded_model[path] = model
            model_dict[path].pop('model')

    if args.get('cli', False):
        cli = Cli()
        cli.start(loaded_model)
    else:
        server = Server()
        server.start(loaded_model, args.get('api_port'), model_dict)


if __name__ == "__main__":
    main()
