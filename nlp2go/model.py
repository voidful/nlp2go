from collections import defaultdict

import nlp2
import tfkit
import torch


class Model:
    def __init__(self):
        self.model = None
        self.maxlen = 512

    def load_model(self, model_path):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        package = torch.load(model_path, map_location=device)

        maxlen = package['maxlen']
        type = package['type'].lower()
        config = package['model_config'] if 'model_config' in package else package['bert']

        print("===model info===")
        print("maxlen", maxlen)
        print("type", type)
        print('==========')

        if "once" in type:
            model = tfkit.gen_once.BertOnce(model_config=config, maxlen=maxlen)
        elif "twice" in type:
            model = tfkit.gen_twice.BertTwice(model_config=config, maxlen=maxlen)
        elif "onebyone" in type:
            model = tfkit.gen_onebyone.BertOneByOne(model_config=config, maxlen=maxlen)
        elif 'classify' in type:
            model = tfkit.classifier.BertMtClassifier(package['task'], model_config=config)
        elif 'tag' in type:
            model = tfkit.tag.BertTagger(package['label'], model_config=config, maxlen=maxlen)
        model = model.to(device)
        model.load_state_dict(package['model_state_dict'], strict=False)

        self.model = model
        self.maxlen = maxlen
        self.type = type

    def predict(self, input, predictor):
        results = defaultdict(list)
        results_map = defaultdict(list)
        if 'classify' in self.type:
            tasks = list(self.model.tasks_detail.keys())
        else:
            tasks = ['default']

        for task in tasks:
            for i in nlp2.sliding_windows(nlp2.spilt_sentence_to_array(input, True), self.maxlen - 10):
                input = " ".join(i)
                result, outprob = self.model.predict(input=input, task=task)
                results[task] += result
                results_map[task].extend(outprob)

        if predictor == 'biotag':
            result_dict = self.biotag2json(results, results_map)
        elif predictor == 'tag':
            result_dict = self.tag2json(results, results_map)
        else:
            result_dict = self.just2json(results, results_map)

        return result_dict

    def just2json(self, result, map):
        result_dict = {
            'result': result,
            'result_map': map
        }
        return result_dict

    def tag2json(self, results, maps):
        result_dict = {
            'result': results,
            'tags': defaultdict(list),
            'result_map': maps
        }
        for task, result in results.items():
            results[task] = "".join(result)

        word_str = ""
        for task, map in maps.items():
            for i in map:
                k = list(i.keys())[0]
                v = list(i.values())[0]
                if v is not "O":
                    word_str += k
                elif len(word_str) > 0:
                    result_dict['tags'][task].append(word_str)
                    word_str = ""

        return result_dict

    def biotag2json(self, results, maps):
        result_dict = {
            'result': results,
            'tags': defaultdict(dict),
            'result_map': maps
        }

        for task, result in results.items():
            results[task] = "".join(result)

        word_str = ""
        word_type = ""
        for task, map in maps.items():
            for i in map:
                k = list(i.keys())[0]
                v = list(i.values())[0]
                if "B" in v and len(word_str) > 0:
                    result_dict['tags'][task][word_str] = word_type
                    word_str = ""
                if v is not "O":
                    word_str += k
                    word_type = v.split("_")[1]
                elif len(word_str) > 0:
                    result_dict['tags'][task][word_str] = word_type
                    word_str = ""

        return result_dict
