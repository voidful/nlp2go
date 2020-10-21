import React from 'react';
import '../App.css';


class PANEL extends React.Component {

    fetch_result() {
        if (!this.state.loading) {
            let new_state = {loading: true}
            new_state[this.state.id + 'result'] = ''
            this.setState(new_state)
            let input_dict = {}
            this.state.component_list.map((name, index) => {
                input_dict[name] = this.state[this.state.id + name]
                return null
            })
            fetch(window.location.origin + "/api?id=" + this.state.id, {
                method: 'POST',
                body: JSON.stringify(input_dict),
                headers: new Headers({
                    'Content-Type': 'application/json'
                })
            })
                .then(res => res.json())
                .then(data => {
                    let dict = {};
                    Object.entries(data).map(function ([key, value]) {
                        dict[key] = value;
                        return null
                    });
                    let new_state = {loading: false};
                    new_state[this.state.id + 'result'] = JSON.stringify(dict, null, 2)
                    this.setState(new_state);
                })
                .catch(e => {
                    console.log(e);
                    this.setState({result: "Error,Plz Try Again."});
                    this.setState({loading: false})
                })
        }
    }

    constructor(props) {
        super(props);
        this.state = {
            loading: false
        }
        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleExampleChange = this.handleExampleChange.bind(this);
    }

    static getDerivedStateFromProps(props, state) {
        let {id, name, description, component, example} = props
        let component_list = []
        component.map((item_dict, index) => (
            component_list.push(item_dict["name"])
        ))
        let state_dict = {
            id: id,
            name: name,
            description: description,
            component: component,
            example: example,
            component_list: component_list,
            loading: state.loading
        }
        state_dict[id + "result"] = state[id + "result"]
        return state_dict
    }

    handleInputChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;
        this.setState({
            [name]: value
        });
    }

    handleExampleChange(event) {
        const target = event.target;
        const value = target.value;
        let temp = {};
        for (let i in this.state.example[value - 1]) {
            temp[this.state.id + i] = this.state.example[value - 1][i];
        }
        this.setState(temp)
    }

    render() {
        return (
            <section id="banner">
                <div className="content">
                    <h2>{this.state.name}</h2>
                    <blockquote>
                        {this.state.description}<br/>
                    </blockquote>
                    <select key={JSON.stringify(this.state.example)} onChange={this.handleExampleChange}>
                        <option value={0}>Example</option>
                        {this.state.example.map((item_dict, index) => (
                            <option key={index} value={1 + index}>{item_dict['name']}</option>
                        ))}
                    </select>
                    <br/>
                    {this.state.component.map((item_dict, index) => (
                        <div key={index}>
                            {(() => {
                                switch (item_dict["type"]) {
                                    case "textarea":
                                        return <textarea name={this.state.id + item_dict["name"]}
                                                         placeholder={item_dict["placeholder"]}
                                                         value={this.state[this.state.id + item_dict["name"]] === undefined ? "" : this.state[this.state.id + item_dict["name"]]}
                                                         onChange={this.handleInputChange}
                                                         rows="6">
                                                    </textarea>
                                    case "input":
                                        return <input name={this.state.id + item_dict["name"]}
                                                      placeholder={item_dict["placeholder"]}
                                                      value={this.state[this.state.id + item_dict["name"]] === undefined ? "" : this.state[this.state.id + item_dict["name"]]}
                                                      type="text"
                                                      onChange={this.handleInputChange}/>
                                    default:
                                        return <br/>
                                }
                            })()}
                            <br/>
                        </div>
                    ))}

                    <ul className="actions">
                        <li><input type="submit" onClick={() => this.fetch_result()} value="Send"
                                   className="primary"/></li>
                    </ul>

                    {this.state.loading === true && (
                        <div className="loading">
                            <span></span>
                            <span></span>
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    )}

                    {this.state[this.state.id + 'result'] &&
                    <div>
                        <h3>Answer:</h3>
                        <pre>
                        <code name="result">{this.state[this.state.id + 'result']}</code>
                        </pre>
                    </div>
                    }
                </div>

            </section>
        );
    }
}

export default PANEL;
