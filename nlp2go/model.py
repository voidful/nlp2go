import tfkit
from transformers import pipeline, pipelines, BertTokenizer
import inquirer
from .parser import *


class Model:

    def __init__(self, model_path, model_task=None, enable_arg_panel=False):
        self.model = None
        if nlp2.is_file_exist(model_path) or "tfkit_" in model_path:  # tfkit models
            self.lib = 'tfkit'
            self.model, self.predict_parameter, self.model_task = self.load_tfkit_model(model_path, model_task,
                                                                                        enable_arg_panel)
        else:  # huggingface's transfromers model - local model saved in dir, online model name without tfkit tag
            self.lib = 'hf'
            self.model, self.predict_parameter, self.model_task = self.load_huggingface_model(model_path, model_task,
                                                                                              enable_arg_panel)

    def load_huggingface_model(self, model_path, model_task=None, enable_arg_panel=False):
        supported_type = list(pipelines.SUPPORTED_TASKS.keys())
        if model_task is None or model_task not in supported_type:
            inquirer_res = inquirer.prompt(
                [inquirer.List('model_task', message="Select model task", choices=supported_type)])
            model_task = inquirer_res['model_task']

        tok_conf = BertTokenizer.from_pretrained(model_path) if 'voidful/albert_chinese' in model_path else model_path
        nlp = pipeline(model_task, model=model_path,
                       tokenizer=tok_conf)
        predict_parameter = {}
        return nlp, predict_parameter, model_task

    def load_tfkit_model(self, model_path, model_task=None, enable_arg_panel=False):
        model = tfkit.load_model(model_path, model_task)
        predict_parameter = tfkit.load_predict_parameter(model, enable_arg_panel=enable_arg_panel)
        model_task = model.__class__.__name__
        return model, predict_parameter, model_task

    def predict(self, argument={}, enable_input_panel=False):
        parser = Parser(self.model_task)
        input_argument = parser.inputParser(argument, enable_input_panel)

        if "wrong" in input_argument:
            return {
                'result': 'incorrect input:' + str(input_argument['wrong']) +
                          ', Should be:' + str(input_argument["all"]),
                'result_info': input_argument
            }
        else:
            if self.lib == 'hf':
                predict_func = self.model
            else:
                predict_func = self.model.predict

            if isinstance(input_argument, str):
                return parser.outputParser(predict_func(input_argument))
            else:
                self.predict_parameter.update(input_argument)
                return parser.outputParser(predict_func(**self.predict_parameter))
