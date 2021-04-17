import React, { useEffect, useState } from 'react'; //, { useState, useEffect } from 'react';
import './App.css';

class SignUpForm extends React.Component {
    constructor(props){
      super(props);
      this.state = {
        firstName: '', 
        pronouns: '', 
        preferences: ''};

      this.handleChange = this.handleChange.bind(this);
    }
  
    handleChange(event) {
      this.setState({[event.target.name]: event.target.value});
    }

    handleSubmit(event) {
      alert('You submitted the form');
      // get form data out of state
     // const { firstName, pronouns, preferences } = this.state;
     console.log("making request")

     fetch('http://localhost:5000/add', {method: "POST"})
  .then(response => response.json())
  .then(data => console.log(data));

    //   fetch('http://localhost:5000/callback' , {
    //     method: "POST",
    //     headers: {
    //       'Content-type': 'application/json'
    //     }
    //    // body: JSON.stringify('')
    //   })
    //   .then((result) =>{
    //     alert('You passed the info');
    //     return result.json();
    //   } )
    //   .then((info) => { console.log(info); })

    //   event.preventDefault();

    }

    onSubmit = (event) => {
       
      alert('You passed the info in onsubmit');
       event.preventDefault();
      // get form data out of state
      const { firstName, pronouns, preferences } = this.state;
      
      fetch('http://localhost:5000/add' , {
        method: "POST",
        headers: {
          'Content-type': 'application/json'
        },
        body: JSON.stringify(this.state)
      })
      .then((result) =>{
        return result.json()
      } )
      .then((info) => { console.log(info); })

    }

    render(){
      const { classes } = this.props;
      const { first_name, pronouns, preferences } = this.state;
      return (

        
        <form onSubmit={this.handleSubmit}>
          <label> First name: 
          <input name="firstName" type="text" value={this.state.first_name} onChange={this.handleChange} />
          </label>
          <br />

          <label> Pronouns: 
          <input name="pronouns" type="text" value={this.state.pronouns} onChange={this.handleChange} />
          </label>
          <br />

          <label> Preferences: 
          <input name="preferences" type="text" value={this.state.preferences} onChange={this.handleChange} />
          </label>
          <br />
          <input type="submit" value="submit" />

        </form>
      );
    }
}


export default SignUpForm;