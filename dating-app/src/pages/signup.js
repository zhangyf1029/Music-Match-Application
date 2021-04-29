import React from 'react';
import { useHistory } from "react-router-dom"; 
import {useState, useEffect } from 'react'
import 'bulma/css/bulma.min.css';
// export const Users = ({ users }) => { return (<div>{movies.length}</div> ) }
    class SignUp extends React.Component {
      constructor(props){
      super(props);
      this.state = {
        url: ''
      };
      this.handleSubmit = this.handleSubmit.bind(this);
      }

      handleSubmit(event){ 
        let data;
        let temp; 

        event.preventDefault();
        console.log('button clicked');
        fetch('http://localhost:5000/authspotify', {
         method: 'get',
        })
        .then( (response) => response.json()
        )
        .then((data) => window.location.href = data.data)
        // .then( window.location.href = 'http://localhost:3000')
        // .then(data => {this.setState({url: data.data})})
      }

    // const res = await fetch('http://localhost:5000/authspotify' , {
    //   method: "POST",
    //   headers: {
    //     'Content-type': 'application/json'
    //   },
    //   body: JSON.stringify(this.state)
    // })
    // const data = await  res.json()

    // setTasks([...tasks, data])
    // .then((result) =>{
    //   return result.json()
    // } )
    // .then((info) => { console.log(info); })

    render(){  return (
      <div class="hero-body">
      <div class="container has-text-centered">
         
        <h1 class="title" >
          Sign Up Today
        </h1>
        <h2 class="subtitle" >
          Using Spotify secure network
        </h2>
      <div class="column is-4 is-offset-4">
          <form action="" onSubmit={this.handleSubmit}>
            <button class="button is-block is-info is-large is-fullwidth">Sign Up With Spotify</button>
          </form>
        </div>
        </div>
        </div>
  );
}
    };
  
  export default SignUp;