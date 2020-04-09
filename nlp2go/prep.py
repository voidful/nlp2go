import argparse
import logging
from collections import defaultdict

import json
from .model import Model


def main():
    global model_dict
    model_dict = defaultdict(dict)
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--json', type=str)
    group.add_argument('--model', type=str)
    args = parser.parse_args()

    if args.model:
        model = Model()
        model.load_model(args.model)
    else:
        with open(args.json, 'r', encoding='utf8') as reader:
            model_dict = json.loads(reader.read())
        for k, v in model_dict.items():
            model = Model()
            model.load_model(model_dict[k]['model'])

    print("==================")
    print("finish pre loading")


if __name__ == "__main__":
    main()
