import re
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
        elif 'qa' in type:
            model = tfkit.qa.BertQA(model_config=config, maxlen=maxlen)

        model = model.to(device)
        model.load_state_dict(package['model_state_dict'], strict=False)

        self.model = model
        self.maxlen = maxlen
        self.type = type

    def predict(self, input, param_dict):
        beamsearch = param_dict.get('beamsearch', False)
        beamsize = param_dict.get('beamsize', 3)
        filtersim = param_dict.get('filtersim', True)
        topP = param_dict.get('topP', 1)
        topK = param_dict.get('topK', 0.7)
        task = param_dict.get('task', None)

        if 'classify' in self.type:
            if task is None:
                print(list(self.model.tasks_detail))
                task = list(self.model.tasks_detail)[0]
        else:
            task = 'default'

        predict_param = {'input': '', 'task': task}
        if beamsearch and 'onebyone' in self.type:
            predict_param['beamsearch'] = beamsearch
            predict_param['beamsize'] = beamsize
            predict_param['filtersim'] = filtersim
        elif 'onebyone' in self.type:
            predict_param['topP'] = topP
            predict_param['topK'] = topK

        predict_func = self.model.predict
        sep = tfkit.utility.tok_sep(self.model.tokenizer)
        sep = sep.replace('[', '\[').replace(']', '\]').replace('<', '\<').replace('>', '\>')
        regex = r"[0-9]+|[a-zA-Z]+\'*[a-z]*|[\w]" + "|" + sep
        input = " ".join(re.findall(regex, input, re.UNICODE))
        predict_param['input'] = input
        predict_param['task'] = task
        result_list, results_dict = predict_func(**predict_param)
        result_dict = self.convert2json(result_list, results_dict)
        return result_dict

    def convert2json(self, result, map):
        result_dict = {
            'result': result,
            'result_info': map
        }
        return result_dict
