# nlp2go - hosting nlp models for demo purpose

## Example
hosting single model
```
nlp2go --model model_path --predictor biotag
```
hosting multiple models
1. create a json file as below:
```json
{
    "API1_PATH": {
      "model": "model1_path",
      "predictor": "predictor_tag"
    },
    "API2_PATH": {
      "model": "model2_path",
      "predictor": "predictor_tag"
    }
}
```
2. run
```
nlp2go --json json_file_path  
```

## Installation

### Installing via pip
```bash
pip install nlp2go
```

## Running nlprep

Once you've installed nlprep, you can run with

`python -m nlp2go.server` # local version  
or  
`nlp2go`  # pip installed version

and the following parameter:
```
$ nlp2go
arguments:
  --model       model path 
  or   
  --json        json file include models setting 
  
  --outdir      processed result output directory       
  
optional arguments:
  -h, --help    show this help message and exit
  --predictor   formatting result on different kind of task    ['biotag', 'tag', 'default']  
  --path api path
  --port api hosting port
```
Json file example
```json
{
    "API1_PATH": {
      "model": "model1_path",
      "predictor": "predictor_tag"
    },
    "API2_PATH": {
      "model": "model2_path",
      "predictor": "predictor_tag"
    }
}
```

## Expose application over the web
I recommend using ngrok to expose this api for demo purpose  
Ngrok: [https://ngrok.com](https://ngrok.com)

