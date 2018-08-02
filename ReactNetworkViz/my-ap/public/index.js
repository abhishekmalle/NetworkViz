import React from 'react';
import ReactDOM from 'react-dom';

class VizBox extends React.Component {
  render(){
    const url = 'http://localhost:5000'
    const result = fetch(url,
        {method:'POST',
        body:'{foo:bar}'}).then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    console.log(myJson);
  });
    console.log(result);
    return(
      <div >lol</div>
    );
  }
}

function submit(){
    console.log('asdafds')
    ReactDOM.render(<VizBox />, document.getElementById("viz"));
    return false
}
