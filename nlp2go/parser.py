from collections import OrderedDict
import nlp2
import tfkit


class Parser:
    def __init__(self, model_type, model):
        self.model = model
        input_mapping = self.INPUT_PARSER_MAPPING
        output_mapping = self.OUTPUT_PARSER_MAPPING
        self.input_parser = input_mapping[model_type] if model_type in input_mapping else input_mapping['general']
        self.output_parser = output_mapping[model_type] if model_type in output_mapping else output_mapping['general']

    def inputParser(self, argument={}, enable_arg_panel=False):
        argument = nlp2.function_argument_panel(self.input_parser, inputted_arg=argument,
                                                disable_input_panel=(not enable_arg_panel))
        # error input check
        miss = nlp2.function_check_missing_arg(self.input_parser, list(argument.keys()))
        if len(miss) > 0:
            return {"wrong": miss, "all": nlp2.function_get_all_arg(self.input_parser)}
        else:
            return self.input_parser(self, **argument)

    def outputParser(self, *outputs):
        return self.output_parser(self, outputs)

    # Specific Model Input Parser
    def inputTfkitGeneralParser(self, input=""):
        return {'input': input}

    def inputHFGeneralParser(self, input="", **pred_arg):
        return input

    def inputHFGenerateParser(self, input="", **pred_arg):
        for key, value in pred_arg.items():
            if 'input' in key:
                input += (tfkit.utility.tok.tok_sep(self.model.tokenizer) + value) if len(input) > 0 else value
        return input

    def inputTfkitQAParser(self, passage="", question=""):
        sep = tfkit.utility.tok.tok_sep(self.model.tokenizer)
        return {'input': passage + sep + question}

    def inputHFQAParser(self, passage="", question=""):
        return {'context': passage, 'question': question}

    # Specific Model Output Parser
    def outputHFGeneralParser(self, result_list):
        answer_list = []
        for r in result_list:
            answer_list.append(r)
        return {'result': answer_list}

    def outputTfkitGeneralParser(self, output):
        (result_list, result_dict) = output[0]
        return {
            'result': result_list,
            'result_info': result_dict
        }

    def outputHFQAParser(self, result_list):
        answer_list = []
        for r in result_list:
            answer_list.append(r['answer'])
        return {'result': answer_list, 'result_info': result_list}

    OUTPUT_PARSER_MAPPING = OrderedDict(
        [
            # Huggingface's model
            ("question-answering", outputHFQAParser,),
            ("feature-extraction", outputHFGeneralParser,),
            ("sentiment-analysis", outputHFGeneralParser,),
            ("ner", outputHFGeneralParser,),
            ("fill-mask", outputHFGeneralParser,),
            ("summarization", outputHFGeneralParser,),
            ("text2text-generation", outputHFGeneralParser,),
            ("translation_xx_to_yy", outputHFGeneralParser,),
            ("zero-shot-classification", outputHFGeneralParser,),
            ("text-generation", outputHFGeneralParser,),
            ("conversational", outputHFGeneralParser,),
            # TFKIT model
            ("general", outputTfkitGeneralParser,),
        ]
    )


    INPUT_PARSER_MAPPING = OrderedDict(
        [
            # Huggingface's model
            ("feature-extraction", inputHFGeneralParser,),
            ("sentiment-analysis", inputHFGeneralParser,),
            ("ner", inputHFGeneralParser,),
            ("question-answering", inputHFQAParser,),
            ("fill-mask", inputHFGeneralParser,),
            ("summarization", inputHFGenerateParser,),
            ("text2text-generation", inputHFGenerateParser,),
            ("translation_xx_to_yy", inputHFGeneralParser,),
            ("zero-shot-classification", inputHFGeneralParser,),
            ("text-generation", inputHFGenerateParser,),
            ("conversational", inputHFGeneralParser,),
            # TFKIT model
            ("qa", inputTfkitQAParser,),
            ("general", inputTfkitGeneralParser,),
        ]
    )
