import unittest

from transformers import pipelines

import nlp2go


class TestModel(unittest.TestCase):

    def test_load_huggingface_model(self):
        nlp, predict_parameter, model_task = nlp2go.Model.load_huggingface_model(self, 'voidful/albert_chinese_tiny',
                                                                                 task='feature-extraction')
        print(nlp, predict_parameter, model_task)
        self.assertTrue(len(predict_parameter) == 0)

        nlp, predict_parameter, model_task = nlp2go.Model.load_huggingface_model(self, 'voidful/albert_chinese_tiny',
                                                                                 task="fill-mask")
        print(nlp, predict_parameter, model_task)
        self.assertTrue(len(predict_parameter) == 0)

    def test_predict_hf(self):
        supported_type = list(pipelines.SUPPORTED_TASKS.keys())
        ignoree_type = ['table-question-answering', 'summarization', 'translation', 'text2text-generation',
                        'text-generation', 'conversational']
        for task in supported_type:
            print(task)
            if task not in ignoree_type:
                model = nlp2go.Model('voidful/albert_chinese_tiny', task=task)
            else:
                continue
            result = model.predict(input="I [MASK] Fine.")
            print(result)
            self.assertIsInstance(result, dict)
            result = model.predict("I [MASK] Fine.")
            print(result)
            self.assertIsInstance(result, dict)
            result = model.predict({"contexta": {"input": "I [MASK] ok.", "order": 0},
                                    "contextb": {"input": "I [MASK] Fine.", "field": "input", "order": 1}})
            print(result)
            self.assertIsInstance(result, dict)

    def test_predict_hf_generate_with_parama(self):
        model = nlp2go.Model('sshleifer/tiny-gpt2', task="text-generation")
        result_dict = model.predict("I [MASK] Fine.", num_return_sequences=3)
        print(result_dict)
        self.assertEqual(len(result_dict['result']), 3)

    def test_predict_hf_qa(self):
        model = nlp2go.Model("sshleifer/tiny-distilbert-base-cased-distilled-squad", task="question-answering")
        result_dict = model.predict(question="How old are you.", context="i am 10 years old")
        print(result_dict)

    def test_predict_tfkit(self):
        # tfkit pipeline
        from nlp2go.modelhub import MODELMAP
        for k in MODELMAP.keys():
            model = nlp2go.Model(k)
            if "mrc" not in k:
                result_dict = model.predict(input="今季新番有咩睇")
                print(result_dict)
                self.assertIsInstance(result_dict, dict)
                result_dict = model.predict("今季新番有咩睇")
                print(result_dict)
                self.assertIsInstance(result_dict, dict)
                result_dict = model.predict({"contexta": {"input": "今季新番有咩睇", "order": 0},
                                             "contextb": {"input": "冇啊", "field": "input", "order": 1}})
                self.assertIsInstance(result_dict, dict)
            else:
                result_dict = model.predict(passage="今季冇新番", question="今季新番有咩睇", topk=10)
                print(result_dict)
                self.assertIsInstance(result_dict, dict)
                result_dict = model.predict({"contexta": {"input": "今季新番有咩睇", "field": "question"},
                                             "contextb": {"input": "今季冇新番", "field": "passage"}})
                print(result_dict)
                self.assertIsInstance(result_dict, dict)

    def test_predict_tfkit_with_parama(self):
        model = nlp2go.Model("tfkit_zh_dream_small")
        result_dict = model.predict("今季新番有咩睇", decodenum=3)
        print(result_dict)
        self.assertTrue(len(result_dict['result']) == 3)
