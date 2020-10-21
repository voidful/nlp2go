<p  align="center">
    <br>
    <img src="https://raw.githubusercontent.com/voidful/nlp2go/master/docs/img/nlp2go.png" width="400"/>
    <br>
</p>
<br/>

# nlp2go web service   
**Hosting nlp models for demo purpose**  

## Showcase
https://demo.voidful.tech

## Feature
There are many additional features :
- Plug and play any model you want.
- Hosting a nlp service with docker-compose.
- Flexible configuration with different layout for different task.

## Documentation
write your own config.json, build your own demo website.
```json
{
"task_id": {
    "model": "model_path_or_name",
    "description": "model description",
    "name": "model display name",
    "component": [
      {
        "name": "api-field-name",
        "type": "widget type - input/textarea",
        "placeholder": "input placeholder"
      }
    ],
    "example": [
      {
        "api-field-name": "model example,key should follow component name",
        "name": "example display name"
      }
    ]
  }
}
```

## Quick Start

### Build project
```bash
docker-compose up --detach --build
```

### Shutdown
```bash
docker-compose down
```

## Contributing
Thanks for your interest.There are many ways to contribute to this project. Get started [here](https://github.com/voidful/nlp2go/blob/master/CONTRIBUTING.md).

## License ![PyPI - License](https://img.shields.io/github/license/voidful/nlp2go)

* [License](https://github.com/voidful/nlp2go/blob/master/LICENSE)

## Icons reference
Icons modify from <a href="https://www.flaticon.com/free-icon/running_2151630" title="Good Ware">Good Ware</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>     
Icons modify from <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>    