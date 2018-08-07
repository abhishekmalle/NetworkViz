import React from 'react';
import ReactDOM from 'react-dom';
import * as vis from "vis";

class TopSide extends React.Component {
    render() {
        return(
            <form>
            <input id="myQuery"></input>
            <button type="button" onClick={() => this.props.onClick()}>submit</button>
            </form>
            );
    }
}

class Root extends React.Component{
    submit() {

        const myQuery = document.getElementById("myQuery").value
        const url = 'http://localhost:5000'
        fetch(url,
        {
            method:'POST',
            body:myQuery
        }).then(function(response) {
            return response.json();
        }).then(myJson => {
            this.setState({nodes:myJson.nodes, links:myJson.links});
        });
        var nodes = new vis.DataSet(this.state.nodes);

        // create an array with edges
        var edges = new vis.DataSet(this.state.links);

          // create a network
        var container = document.getElementById('viz');
        var data = {
            nodes: nodes,
            edges: edges
        };
        var options = {};
        var network = new vis.Network(container, data, options);
        console.log(this.state.links)
    }


constructor(props) {
    super(props);
    this.state = {
        nodes: null,
        links: null
    };
}

render(){
    return(
        <div className="root">
        <TopSide state={this.state} onClick={()=>this.submit()}/>
        <div id="viz" height="800" width="800"></div>
        </div>
        );
}
}

//------------------------//
ReactDOM.render(<Root />, document.getElementById("root"));
