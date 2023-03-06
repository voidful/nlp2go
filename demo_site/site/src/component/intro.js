import React from 'react';
import '../App.css';


function Intro() {
    return (
        <section id="banner">
            <div className="content">
                <header>
                    <h1>NLP2GO Demo Website</h1>
                    <p>Simple is powerful</p>
                </header>
                <ps>Explore different models by selecting them from the left menu.</ps>
            </div>
            <span className="image object"><img
                src="https://raw.githubusercontent.com/voidful/nlp2go/master/docs/img/nlp2go.png" alt="nlp2go"/>
            </span>
        </section>
    );
}

export default Intro;
