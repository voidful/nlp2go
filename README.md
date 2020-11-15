<p  align="center">
    <br>
    <img src="https://raw.githubusercontent.com/voidful/nlp2go/master/docs/img/nlp2go.png" width="400"/>
    <br>
</p>
<br/>
<p align="center">
    <a href="https://pypi.org/project/nlp2go/">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/nlp2go">
    </a>
    <a href="https://github.com/voidful/nlp2go">
        <img alt="Download" src="https://img.shields.io/pypi/dm/nlp2go">
    </a>
    <a href="https://github.com/voidful/nlp2go">
        <img alt="Build" src="https://img.shields.io/github/workflow/status/voidful/nlp2go/Python package">
    </a>
    <a href="https://github.com/voidful/nlp2go">
        <img alt="Last Commit" src="https://img.shields.io/github/last-commit/voidful/nlp2go">
    </a>
</p>
<br/>

## nlp2go   
**Hosting nlp models in one line**  

### Demo
[demo website](https://demo.voidful.tech)

### Introduction
Once the model is trained, we want to verify our model as quickly as possible.
nlp2go provides a CLI interface and  Restful api that allows you to quickly deploy model to everyone.

### Feature
There are many additional features :
- Support loading multiple models at a time.
- Provide input format checking.
- You can also load models in python code.
- Flexible handling of parameters so that parameter can be changed in each prediction.
- Support huggingface transformers’s model
- There are models in the Model Hub for you to try  

# Documentation
Learn more from the [docs](https://voidful.github.io/nlp2go/).  

## Quick Start

### Installing via pip
```bash
pip install nlp2go
```

### hosting single model
```
nlp2go --model model_path 
```
### hosting multiple models
1. create a json file as below:
```json
{
    "API1_PATH": {
      "model": "model1_path"
    },
    "API2_PATH": {
      "model": "model2_path"
    }
}
```
2. run
```
nlp2go --json json_file_path  
```
**You can also try nlp2go in Google Colab: [![Google Colab](https://colab.research.google.com/assets/colab-badge.svg "nlp2go")](https://colab.research.google.com/drive/15aYFPsa88A20g5R2QS3kyVrjGlccr0Qd?usp=sharing)**


## Contributing
Thanks for your interest.There are many ways to contribute to this project. Get started [here](https://github.com/voidful/nlp2go/blob/master/CONTRIBUTING.md).

## License ![PyPI - License](https://img.shields.io/github/license/voidful/nlp2go)

* [License](https://github.com/voidful/nlp2go/blob/master/LICENSE)

## Icons reference
Icons modify from <a href="https://www.flaticon.com/free-icon/running_2151630" title="Good Ware">Good Ware</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>     
Icons modify from <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>    
