import json
from nlp2go.util import NumpyEncoder


class Cli:

    def start(self, models):
        while True:
            for path, model in models.items():
                result_dict = model.predict(enable_input_panel=True)
                print(json.dumps(result_dict['result'], ensure_ascii=False, cls=NumpyEncoder, indent=4, sort_keys=True))
