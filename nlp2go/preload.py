import argparse
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
        Model(args.model)
    else:
        with open(args.json, 'r', encoding='utf8') as reader:
            model_dict = json.loads(reader.read())
        for k, v in model_dict.items():
            task = model_dict[k]['task'] if 'task' in model_dict[k] else None
            Model(model_dict[k]['model'], model_task=task)

    print("==================")
    print("finish pre loading")


if __name__ == "__main__":
    main()
