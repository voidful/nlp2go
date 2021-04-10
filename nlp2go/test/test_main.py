import unittest

import nlp2go


class TestMain(unittest.TestCase):

    def test_parser(self):
        input_arg, model_arg = nlp2go.parse_args(['--model', 'voidful/albert_chinese_tiny', '--task', 'clas'])
        print(input_arg, model_arg)
