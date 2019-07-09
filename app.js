
import logo from "./logo.svg";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

class App extends Component{
    render(){
        return (

            <div className="container">
            <div className="row">
            <div className="col-6"> Column 1</div>
                <header className="App-header">
                <img src={logo}className="App-logo" alt="logo"/>
                <p>
                    Edit <code> src/App.js</code> and save to reload
                </p>
                <a classname="App-link"
                    href="https://angiechangpagne.com"
                    target="_blank"
                    rel="noopener noreferrer">


                    </a>
                    </header>
                    </div>
            </div>


        )
    }
}