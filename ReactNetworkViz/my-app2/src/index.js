import React from 'react';
import ReactDOM from 'react-dom';
import * as d3 from "d3";


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
                    this.setState({graph:{nodes:myJson.nodes, links:myJson.links}});
                });

    console.log(this.state)
    var svg = d3.select("#viz"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

    var color = d3.scaleOrdinal(d3.schemeCategory10);

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function(d) { return d.id; }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    var link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(this.state.graph.links)
        .enter().append("line");

    var node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(this.state.graph.nodes)
        .enter().append("circle")
        .attr("r", 5)
        .attr("fill", function(d) { return color(d.group); })
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    node.append("title")
        .text(function(d) { return d.id; });

    simulation
        .nodes(this.state.graph.nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(this.state.graph.links);

    function ticked() {
        link
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
    };

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }
        }

    constructor(props) {
        super(props);
        this.state = {
            graph:{}
        };
    }

        render(){
            return(
                <div className="root">
                <TopSide state={this.state} onClick={()=>this.submit()}/>
                <svg id="viz" height="800" width="800"></svg>
                </div>
                );
        }
        }

        //------------------------//
        ReactDOM.render(<Root />, document.getElementById("root"));
