import json

from nlp2go.util import NumpyEncoder


class Cli:

    def start(self, models):
        while True:
            for path, model in models.items():
                model.enable_panel = True
                result_dict = model.predict()
                print(json.dumps(result_dict, ensure_ascii=False, cls=NumpyEncoder, indent=4, sort_keys=True))
