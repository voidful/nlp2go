import re
import tfkit
import torch
from transformers import BertTokenizer, AutoTokenizer, AutoModel


class Model:
    def __init__(self):
        self.model = None
        self.maxlen = 512

    def load_model(self, model_path, model_type=None):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        package = torch.load(model_path, map_location=device)

        maxlen = package['maxlen']
        config = package['model_config'] if 'model_config' in package else package['bert']
        model_types = [package['type']] if not isinstance(package['type'], list) else package['type']
        models_state = package['models'] if 'models' in package else [package['model_state_dict']]

        print("===model info===")
        print("maxlen", maxlen)
        print("type", model_types)
        print("config", config)
        print('==========')

        # load pre-train model
        if 'albert_chinese' in config:
            tokenizer = BertTokenizer.from_pretrained(config)
        else:
            tokenizer = AutoTokenizer.from_pretrained(config)
        pretrained = AutoModel.from_pretrained(config)

        type = model_types[0] if model_type is None else model_type

        if "once" in type:
            model = tfkit.gen_once.Once(tokenizer, pretrained, maxlen=maxlen)
        elif "twice" in type:
            model = tfkit.gen_twice.Twice(tokenizer, pretrained, maxlen=maxlen)
        elif "onebyone" in type:
            model = tfkit.gen_onebyone.OneByOne(tokenizer, pretrained, maxlen=maxlen)
        elif 'classify' in type:
            model = tfkit.classifier.MtClassifier(package['task'], tokenizer, pretrained)
        elif 'tag' in type:
            model = tfkit.tag.Tagger(package['label'], tokenizer, pretrained, maxlen=maxlen)
        elif 'qa' in type:
            model = tfkit.qa.QA(tokenizer, pretrained, maxlen=maxlen)

        model = model.to(device)
        model.load_state_dict(models_state[model_types.index(type)], strict=False)

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
        regex = r"\[Question\]|[0-9]+|[a-zA-Z]+\'*[a-z]*|[\w\W]" + "|" + sep
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
