#Usage
## Overview
```
$ nlp2go
arguments:

either json config or model path
  --model       model path 
  or   
  --json        json file include models setting      
  
optional arguments:
  -h, --help    show this help message and exit
  --enable_arg_panel   enable argument input panel
  --path        restful api path
  --port        restful api hosting port
  --cli         enable command line interface(default using restful api)
```

## Load Model
### load TFkit models
#### online model
```
nlp2go --model model_name_from_models_hub --cli
```
#### local model
```
nlp2go --model model_path.pt --cli
```

### load Huggingface's transformers models
#### online model
```
nlp2go --model model_name_from_https://huggingface.co 
--task  any of it:[feature-extraction, sentiment-analysis, ner, question-answering, fill-mask, summarization, translation_en_to_fr, translation_en_to_de, translation_en_to_ro, text-generation]
--cli
```
example:
```
nlp2go --model voidful/albert_chinese_tiny --task fill-mask --cli 
```
#### local model
```
nlp2go --model model_dir
--task  any of it:[feature-extraction, sentiment-analysis, ner, question-answering, fill-mask, summarization, translation_en_to_fr, translation_en_to_de, translation_en_to_ro, text-generation]
--cli
```

### load multiple models
For deploying multiple model to restful api, nlp2go needs to load models from a json config file.
```
nlp2go
--json  json_config_path
--cli
```
json format:  
```json
{
    "API1_PATH": {
      "model": "model1_path or name",
      "model_parameter": "argument"
    },
    "API2_PATH": {
      "model": "model1_path or name",
      "model_parameter": "argument"
    }
}
```
Example:   
`./test_conf.json`
```json
{
    "albert_mask": {
      "model": "voidful/albert_chinese_tiny",
      "task": "fill-mask"
    }
}
```
run  
```bash
nlp2go --json ./test_conf.json --api_port 3000
```
result
```text
hosting api in path: /api/+ ['albert_mask']
Model loaded, serving demo on port 3000
```
test
```text
Get: localhost:3000/api/albert_mask?input=今天[MASK]情很好
```

### pre-load models
`nlp2go-preload` is to pre-download model files when we host our models using docker.
that can avoid downloading model at run time
```bash
nlp2go-preload --json config.json
```
example dockerfile
```dockerfile
FROM pytorch/pytorch:latest
RUN apt-get -y update

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy source project
COPY . /usr/src/app/

RUN pip install nlprep tfkit nlp2go -U
RUN nlp2go-preload --json config.json
CMD PYTHONIOENCODING=utf8 nlp2go --json config.json --port ${PORT}
```

## Model Interface

### Command Line Interface
model predict using command line interface(cli)
```bash
nlp2go --model voidful/albert_chinese_tiny --task fill-mask --cli 
```
argument:   
`--enable_arg_panel`  to enable a input panel that let you input argument

### Restful API
```bash
nlp2go --model voidful/albert_chinese_tiny --task fill-mask --api_path model --api_port 3000
```
argument:   
`--enable_arg_panel`  to enable a input panel that let you input argument    
`--api_path path` set API path after 'host/API/'   
`--api_port` set hosting port   

####api detail:  
#####url  
    `host/API/path`  
#####method  
    `GET` | `POST`  
#####url Params 

by default   
```
input=[string] 
``` 

task specific eg: QA   
```
context[string]  
question=[string]
```
     

### Python code
```python
import nlp2go
albert_fillmask = nlp2go.Model(model_path="voidful/albert_chinese_tiny",model_task="fill-mask")
albert_fillmask.predict({"input":"今天[MASK]情很好"})
```
result
```json
{'result': [[{'sequence': '[CLS] 今 天 感 情 很 好 [SEP]', 'score': 0.40312328934669495, 'token': 2697, 'token_str': '感'}, {'sequence': '[CLS] 今 天 爱 情 很 好 [SEP]', 'score': 0.1470295488834381, 'token': 4263, 'token_str': '爱'} '[CLS] 今 天 表 情 很 好 [SEP]', 'score': 0.0740746483206749, 'token': 6134, 'token_str': '表'}, {'sequence': '[CLS] 今 天 心 情 很 好 [SEP]', 'score': 0.06646344810724258, 'token': 2552, 'token_str': '心'}, {'sequence': '[CLS] 今 ', 'score': 0.02915295772254467, 'token': 4178, 'token_str': '热'}]]}
```