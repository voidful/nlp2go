import argparse
from collections import defaultdict

import json

from nlp2go import parse_args
from nlp2go.model import Model


def main(arg=None):
    global model_dict
    model_dict = defaultdict(dict)
    args, others_arg = parse_args(arg)

    if args.get('model', None):
        Model(args.get('model'), args.get('panel', False), **others_arg)
    else:
        with open(args.get('json'), 'r', encoding='utf8') as reader:
            model_dict = json.loads(reader.read())
        for path, d in model_dict.items():
            Model(model_dict[path]['model'], args.get('panel', False), **model_dict[path])

    print("==================")
    print("finish pre loading")


if __name__ == "__main__":
    main()
