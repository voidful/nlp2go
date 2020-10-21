import re
from collections import OrderedDict
import nlp2
import tfkit


class Parser:
    def __init__(self, model_type, model):
        self.model = model
        self.input_parser = self.INPUT_PARSER_MAPPING[model_type]
        self.output_parser = self.OUTPUT_PARSER_MAPPING[model_type]

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

    def inputHFGeneralParser(self, input=""):
        return input

    def inputTfkitQAParser(self, passage="", question=""):
        sep = tfkit.utility.tok_sep(self.model.tokenizer)
        return {'input': passage + sep + question}

    def inputHFQAParser(self, context="", question=""):
        return {'context': context, 'question': question}

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
            ("feature-extraction", outputHFGeneralParser,),
            ("sentiment-analysis", outputHFGeneralParser,),
            ("ner", outputHFGeneralParser,),
            ("question-answering", outputHFQAParser,),
            ("fill-mask", outputHFGeneralParser,),
            ("summarization", outputHFGeneralParser,),
            ("translation_en_to_fr", outputHFGeneralParser,),
            ("translation_en_to_de", outputHFGeneralParser,),
            ("translation_en_to_ro", outputHFGeneralParser,),
            ("text-generation", outputHFGeneralParser,),
            # TFKIT model
            ("Tagger", outputTfkitGeneralParser,),
            ("QA", outputTfkitGeneralParser,),
            ("Twice", outputTfkitGeneralParser,),
            ("OneByOne", outputTfkitGeneralParser,),
            ("Once", outputTfkitGeneralParser,),
            ("BiDiOneByOne", outputTfkitGeneralParser,),
            ("MtClassifier", outputTfkitGeneralParser,),
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
            ("summarization", inputHFGeneralParser,),
            ("translation_en_to_fr", inputHFGeneralParser,),
            ("translation_en_to_de", inputHFGeneralParser,),
            ("translation_en_to_ro", inputHFGeneralParser,),
            ("text-generation", inputHFGeneralParser,),
            # TFKIT model
            ("Tagger", inputTfkitGeneralParser,),
            ("QA", inputTfkitQAParser,),
            ("Twice", inputTfkitGeneralParser,),
            ("OneByOne", inputTfkitGeneralParser,),
            ("Once", inputTfkitGeneralParser,),
            ("BiDiOneByOne", inputTfkitGeneralParser,),
            ("MtClassifier", inputTfkitGeneralParser,),
        ]
    )
