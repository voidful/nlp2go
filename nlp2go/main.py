import argparse
from collections import defaultdict
import json

from .cli import Cli
from .model import Model
from .server import Server


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
    parser.add_argument('--enable_arg_panel', action='store_true', help='enable panel to input argument')
    parser.add_argument('--task', type=str)
    # interface
    parser.add_argument('--api_path', type=str, default="model", help='api path to serve the demo')
    parser.add_argument('--api_port', type=int, default=3000, help='port to serve the demo on')
    parser.add_argument('--cli', action='store_true', help='commandline mode')

    args = parser.parse_args()

    if args.model:
        model_dict[args.api_path] = Model(args.model, args.task, args.enable_arg_panel)
    else:
        with open(args.json, 'r', encoding='utf8') as reader:
            model_dict = json.loads(reader.read())

        for path, d in model_dict.items():
            task = model_dict[path]['task'] if 'task' in model_dict[path] else None
            model = Model(model_dict[path]['model'], task, args.enable_arg_panel)
            model_dict[path] = model

    if args.cli:
        cli = Cli()
        cli.start(model_dict)
    else:
        server = Server()
        server.start(model_dict, args.api_port)


if __name__ == "__main__":
    main()
