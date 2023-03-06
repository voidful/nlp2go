import React from 'react';
import '../App.css';

class Sidebar extends React.Component {

    selected(id) {
        this.props.selected(id)
    }

    render() {
        let {ids = [], names = []} = this.props
        return (
            <div id="sidebar">
                <div className="inner">

                    <nav className="menu">
                        <ul>
                            <li><a href="#home" onClick={() => this.selected('default')}>HOME</a></li>
                        </ul>
                    </nav>

                    <nav className="menu">
                        <header className="major">
                            <h2>MODEL</h2>
                        </header>
                        <ul>
                            {ids.map((id, index) => (
                                <li key={id + index}><a href={"#" + names[index]}
                                                        onClick={() => this.selected(id)}>{names[index]}</a></li>
                            ))}
                        </ul>
                    </nav>

                    {/*<nav className="menu">*/}
                    {/*    <header className="major">*/}
                    {/*        <h2>Reference</h2>*/}
                    {/*    </header>*/}
                    {/*    <ul>*/}
                    {/*        <li><a href="https://github.com/voidful/NLPrep" target="_blank"*/}
                    {/*               rel="noopener noreferrer">nlprep</a></li>*/}
                    {/*        <li><a href="https://github.com/voidful/TFkit" target="_blank"*/}
                    {/*               rel="noopener noreferrer">tfkit</a></li>*/}
                    {/*        <li><a href="https://github.com/voidful/nlp2go" target="_blank"*/}
                    {/*               rel="noopener noreferrer">nlp2go</a></li>*/}
                    {/*    </ul>*/}
                    {/*</nav>*/}

                    <footer id="footer">
                        <p className="copyright">&copy; Voidful. All rights reserved. <br/>
                            Design:<a href="https://html5up.net">HTML5 UP</a>.</p>
                    </footer>

                </div>
            </div>
        );
    }
}

export default Sidebar;
