import React from 'react'; //, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';


class SignUpForm extends React.Component {
    constructor(props){
      super(props);
      this.state = {firstName: null, pronouns: null, preferences: null};

      this.handleChange = this.handleChange.bind(this);
    }
  
    handleChange(event) {
      this.setState({value: event.target.value});
    }

    render(){
      return (
        <form>
          <label> First name: 
          <input name="firstName" type="text" value={this.state.firstName} onChange={this.handleChange} />
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

        </form>
      );
    }
}


export default SignUpForm;