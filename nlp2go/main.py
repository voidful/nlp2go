import argparse
from collections import defaultdict
import json

from .cli import Cli
from .model import Model
from .server import Server

import os

os.environ["PYTHONIOENCODING"] = "utf-8"


def main():
    """
    loading argument and starting an model interface
    """
    global model_dict
    model_dict = defaultdict(dict)
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--json', type=str)
    group.add_argument('--model', type=str)
    parser.add_argument("--config", type=str, help='pre-trained model path after add token')
    parser.add_argument('--enable_arg_panel', action='store_true', help='enable panel to input argument')
    parser.add_argument('--task', type=str)
    # interface
    parser.add_argument('--api_path', type=str, default="model", help='api path to serve the demo')
    parser.add_argument('--api_port', type=int, default=3000, help='port to serve the demo on')
    parser.add_argument('--cli', action='store_true', help='commandline mode')

    args, unknown = parser.parse_known_args()
    loaded_model = {}
    if args.model:
        loaded_model[args.api_path] = Model(args.model, args.config, args.task, args.enable_arg_panel)
    else:
        with open(args.json, 'r', encoding='utf8') as reader:
            model_dict = json.loads(reader.read())

        for path, d in model_dict.items():
            task = model_dict[path]['task'] if 'task' in model_dict[path] else None
            model = Model(model_dict[path]['model'], model_task=task, enable_arg_panel=args.enable_arg_panel)
            loaded_model[path] = model
            model_dict[path].pop('model')

    if args.cli:
        cli = Cli()
        cli.start(loaded_model)
    else:
        server = Server()
        server.start(loaded_model, args.api_port, model_dict)


if __name__ == "__main__":
    main()
