from collections import OrderedDict, defaultdict
import nlp2
import tfkit


class Parser:
    def __init__(self, model_type, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        im = self.INPUT_PARSER_MAPPING
        om = self.OUTPUT_PARSER_MAPPING
        self._input_parser = im[model_type] if model_type in im else im['general']
        self._output_parser = om[model_type] if model_type in om else om['general']

    def input_parser(self, argument={}, enable_arg_panel=False):
        argument = nlp2.function_argument_panel(self._input_parser, inputted_arg=argument,
                                                disable_input_panel=(not enable_arg_panel))
        # error input check
        miss = nlp2.function_check_missing_arg(self._input_parser, list(argument.keys()))
        if len(miss) > 0:
            return {"miss": miss, "all": nlp2.function_get_all_arg(self._input_parser)}
        else:
            return self._input_parser(self, **argument)

    def get_input_parser(self):
        return self._input_parser

    def _input_general_parser(self, input="", **pred_arg):
        input_dict = defaultdict(lambda: OrderedDict())
        for k, v in list(pred_arg.items()):
            if isinstance(v, dict):
                input_dict[v.get('field', 'input')][v.get('order', 0)] = v.get('input')
                pred_arg.pop(k)
        for k, v in input_dict.items():
            if k not in pred_arg:
                pred_arg[k] = ""
            pred_arg[k] += tfkit.utility.tok.tok_sep(self.tokenizer).join(v.values())
        if "input" in pred_arg:
            input = pred_arg["input"]
            pred_arg.pop("input")
        return input, pred_arg

    def _input_hf_fillmask_parser(self, input="", targets=None, top_k=5, **pred_arg):
        param = {"targets": targets, "top_k": top_k}
        param.update(pred_arg)
        input, param = self._input_general_parser(input, **param)
        return input, param

    def _input_hf_generate_parser(self, input="", max_length=20, min_length=10, num_return_sequences=1, num_beams=1,
                                  **pred_arg):
        param = {"max_length": max_length, "min_length": min_length, "num_return_sequences": num_return_sequences,
                 "num_beams": num_beams}
        param.update(pred_arg)
        input, param = self._input_general_parser(**param)
        return input, param

    def _input_hf_qa_parser(self, passage="", question="", **pred_arg):
        param = {"context": passage, "question": question}
        param.update(pred_arg)
        input, param = self._input_general_parser(**param)
        return input, param

    def _input_tfkit_qa_parser(self, passage="", question="", **pred_arg):
        _, param = self._input_general_parser(**pred_arg)
        if "passage" in param:
            passage = param["passage"]
            param.pop("passage", None)
        if "question" in param:
            question = param["question"]
            param.pop("question", None)
        sep = tfkit.utility.tok.tok_sep(self.tokenizer)
        param['input'] = passage + sep + question
        return param

    def output_parser(self, outputs):
        return self._output_parser(self, outputs)

    def _outout_tfkit_parser(self, result_triple):
        result, detail = result_triple
        return {
            'result': result
        }

    def _outout_hf_parser(self, result):
        return {
            'result': result
        }

    OUTPUT_PARSER_MAPPING = OrderedDict(
        [
            # Huggingface's model
            ("question-answering", _outout_hf_parser,),
            ("feature-extraction", _outout_hf_parser,),
            ("sentiment-analysis", _outout_hf_parser,),
            ("ner", _outout_hf_parser,),
            ("fill-mask", _outout_hf_parser,),
            ("summarization", _outout_hf_parser,),
            ("text2text-generation", _outout_hf_parser,),
            ("translation_xx_to_yy", _outout_hf_parser,),
            ("zero-shot-classification", _outout_hf_parser,),
            ("text-generation", _outout_hf_parser,),
            ("conversational", _outout_hf_parser,),
            # TFKIT model
            ("general", _outout_tfkit_parser,),
        ]
    )

    INPUT_PARSER_MAPPING = OrderedDict(
        [
            # Huggingface's model
            ("feature-extraction", _input_general_parser,),
            ("sentiment-analysis", _input_general_parser,),
            ("ner", _input_general_parser,),
            ("question-answering", _input_hf_qa_parser,),
            ("fill-mask", _input_hf_fillmask_parser,),
            ("summarization", _input_hf_generate_parser,),
            ("text2text-generation", _input_hf_generate_parser,),
            ("translation_xx_to_yy", _input_general_parser,),
            ("zero-shot-classification", _input_general_parser,),
            ("text-generation", _input_hf_generate_parser,),
            ("conversational", _input_hf_generate_parser,),
            # TFKIT model
            ("qa", _input_tfkit_qa_parser,),
            ("general", _input_general_parser,),
        ]
    )
