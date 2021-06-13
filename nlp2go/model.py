import inspect

import nlp2
import tfkit
from transformers import pipeline, pipelines, BertTokenizer, cached_path, AutoTokenizer

from nlp2go.modelhub import MODELMAP
from nlp2go.parser import Parser


class Model:

    def __init__(self, model_path, panel=False, **param):
        self.model = None
        self.enable_panel = panel
        if nlp2.is_file_exist(model_path) or "tfkit_" in model_path:  # tfkit models
            self.lib = 'tfkit'
            self.model, self.predict_parameter, self.model_task = self.load_tfkit_model(model_path, **param)
            self.predict_func = self.model.predict
        else:  # huggingface's transfromers model - local model saved in dir, online model name without tfkit tag
            self.lib = 'hf'
            self.model, self.predict_parameter, self.model_task = self.load_huggingface_model(model_path, **param)
            self.predict_func = self.model
        self.parser = Parser(self.model_task, self.predict_func, self.model.tokenizer)
        predict_parameter, _ = nlp2.function_sep_suit_arg(self.parser.get_input_parser(), param)
        self.predict_parameter.update(predict_parameter)
        print("loaded model predict_parameter", predict_parameter)

    def load_huggingface_model(self, model_path, **param):
        supported_type = list(pipelines.SUPPORTED_TASKS.keys())
        if 'task' not in param or param['task'] not in supported_type:
            panel = nlp2.Panel()
            panel.add_element('task', supported_type, "Select model task: ", default={})
            model_task = panel.get_result_dict()['task']
        else:
            model_task = param['task']

        param['model'] = model_path
        param['tokenizer'] = BertTokenizer.from_pretrained(model_path) if 'voidful/albert_chinese' in model_path \
            else AutoTokenizer.from_pretrained(model_path)
        pipeline_param, _ = nlp2.function_sep_suit_arg(pipeline, param)
        nlp = pipeline(**pipeline_param)
        predict_parameter, _ = nlp2.function_sep_suit_arg(nlp, param)
        return nlp, predict_parameter, model_task

    def load_tfkit_model(self, model_path, **param):
        model_task = param['task'] if 'task' in param else None
        model_path = MODELMAP[model_path] if model_path in MODELMAP else model_path
        model, model_task, model_class = tfkit.utility.model_loader.load_trained_model(cached_path(model_path),
                                                                                       tag=model_task)
        predict_parameter, _ = nlp2.function_sep_suit_arg(model.predict, param)
        model.eval()
        return model, predict_parameter, model_task

    def predict(self, pred_json=None, **argument):
        pred_param = self.predict_parameter.copy()
        pred_param.update(argument)
        if pred_json:
            if isinstance(pred_json, str):
                pred_param.update({'input': pred_json})
            else:
                pred_param.update(pred_json)
        input_argument = self.parser.input_parser(pred_param, enable_arg_panel=self.enable_panel)
        try:
            if isinstance(input_argument, tuple):
                pred = self.predict_func(input_argument[0], **input_argument[1])
            else:
                pred = self.predict_func(**input_argument)
            pred = self.parser.output_parser(pred)
            return pred
        except Exception as e:
            return {
                "input": input_argument,
                "error": str(e)
            }
