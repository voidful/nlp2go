<p  align="center">
    <br>
    <img src="https://raw.githubusercontent.com/voidful/nlp2go/master/doc/img/nlp2go.png" width="400"/>
    <br>
<p>
<br/>
<p align="center">
    <a href="https://pypi.org/project/nlp2go/">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/nlp2go">
    </a>
    <a href="https://github.com/voidful/nlp2go">
        <img alt="Download" src="https://img.shields.io/pypi/dm/nlp2go">
    </a>
    <a href="https://github.com/voidful/nlp2go">
        <img alt="Size" src="https://img.shields.io/github/repo-size/voidful/nlp2go">
    </a>
</p>
<br/>

hosting nlp models in one line

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
  --path        api path
  --port        api hosting port
  --cli         command line mode
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
ngrok: [https://ngrok.com](https://ngrok.com)

