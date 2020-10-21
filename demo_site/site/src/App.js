import React from 'react';
import './App.css';
import Sidebar from './component/sidebar.js';
import Intro from "./component/intro.js";
import Header from "./component/header.js";
import PANEL from "./component/panel";

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            selected: "default"
        };

    }

    componentDidMount() {
        this.setState({isLoading: true});
        fetch(window.location.origin + "/config")
            .then(response => response.json())
            .then(data => this.setState({
                data: data, choices: Object.keys(data), name: Object.keys(data).map((key, index) => (
                    data[key].name)), isLoading: false
            }))
    }

    selected(id) {
        this.setState({"selected": id});
        this.setState({"selected_item": this.state.data[id]});
    }

    render() {
        return (
            <div id="wrapper">
                <div id="main">
                    <div className="inner">
                        <Header selected={this.selected.bind(this)}/>
                        {(() => {
                            if (this.state.selected === 'default') {
                                return <Intro/>;
                            } else {
                                return <PANEL
                                    id={this.state.selected}
                                    name={this.state.selected_item.name}
                                    description={this.state.selected_item.description}
                                    component={this.state.selected_item.component}
                                    example={this.state.selected_item.example}
                                />;
                            }
                        })()}
                    </div>

                </div>
                <Sidebar selected={this.selected.bind(this)} ids={this.state.choices} names={this.state.name}/>
            </div>
        );
    }
}

export default App;
