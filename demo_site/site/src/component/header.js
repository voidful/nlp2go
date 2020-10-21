import React from 'react';
import '../App.css';


class Header extends React.Component {

    selected(id) {
        this.props.selected(id)
    }

    render() {
        return (
            <header id="header">
                <p className="logo">
                    <strong>NLP2GO</strong> DEMO</p>
            </header>
        );
    }
}

export default Header;
