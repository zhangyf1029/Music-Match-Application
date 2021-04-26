import React, { useEffect, useState } from 'react'; //, { useState, useEffect } from 'react';
import Header from './Components/Header'
import HandleSubmit from './Components/HandleSubmit'
import Navbar from './Components/Navbar/index'
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'
import Home from './pages'
import About from './pages/about'
import Contact from './pages/contact'
import Signup from './pages/signup'
import Start from './pages/start'
import Users from './Components/Users'


const SignUpForm = () => {
  const [info, setTasks] = useState([])
  const [users, setUsers] = useState([])

  useEffect (() => {
    // const getTasks = async () => {
    //   const tasksFromServer = await fetchTasks() 
    //   setTasks(tasksFromServer)
    // fetch("/getAllUsers").then(response => response.json().then(data => {setUsers(data.users);})); 

  //   getTasks()
  }, [])

  // const fetchTasks = async() => {
  //   const rest = await fetch ('http://localhost:5000/callback')
  //   const data = await rest.json()
  
  //   return data
  // }

  // const add = async(task) => {
  //   const res = await fetch('http://localhost:5000/add', {
  //     method: 'POST',
  //     headers: {
  //     'Content-type': 'application/json'
  //     },
  //     body: JSON.stringify(task)
  //   })

  //   const data = await  res.json()
  //   setTasks([...info, data])


  //   // const id = Math.floor(Math.random() * 10000) + 1 
  //   // const newTask = { id, ...task}
  //   // setTasks([...tasks, newTask])
  // }

  var background = {
    backgroundColor : '#00d1b2',
    color : 'black',
    top: 0,
    height: '100vh',
  }

  // console.log(users);

  return (
    // <div className="App">
    //   <Users users={users.map(users => <div>{users.email} <div>{users.first_name}</div> </div> )} />
    // </div>
    <html>
      <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.2/css/bulma.min.css" />
        {/* <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" 
        rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous" />
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" 
        integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script> */}
      </head>
      <body style= {background}>
        <Router>
          <Navbar />
          <switch>
            <Route path ="/" exact component={Home}/>
            <Route path ="/about" component={About} />
            <Route path ="/start" component={Start} />
            <Route path ="/contact" component={Contact} />
            <Route path ="/signup" component={Signup} />
          </switch>
          {/* <div className="container" style={{backgroundColor: "white"}}>
            <Header />
            <HandleSubmit onAdd={add}/>
          </div> */}

        </Router>
       </body>
     </html>
  );
}

export default SignUpForm;

// class SignUpForm extends React.Component {
//     constructor(props){
//       super(props);
//       this.state = {
//         firstName: '', 
//         pronouns: '', 
//         preferences: ''};

//       this.handleChange = this.handleChange.bind(this);
//     }
  
//     handleChange(event) {
//       this.setState({[event.target.name]: event.target.value});
//     }

//   const handleSubmit = asynch(task) => {
//       //alert('You submitted the form');
//       // get form data out of state
//      // const { firstName, pronouns, preferences } = this.state;
//      console.log("making request")
//      alert('You passed the info in onsubmit');
//      event.preventDefault();
//     // get form data out of state
//   //const { firstName, pronouns, preferences } = this.state;
//     const res = await fetch('http://localhost:5000/add' , {
//       method: "POST",
//       headers: {
//         'Content-type': 'application/json'
//       },
//       body: JSON.stringify(this.state)
//     })
//     const data = await  res.json()
//     setTasks([...tasks, data])
//     // .then((result) =>{
//     //   return result.json()
//     // } )
//     // .then((info) => { console.log(info); })

//   }
     

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

    

//     onSubmit = (event) => {
       
//       alert('You passed the info in onsubmit');
//        event.preventDefault();
//       // get form data out of state
//       const { firstName, pronouns, preferences } = this.state;
      
//       fetch('http://localhost:5000/add' , {
//         method: "POST",
//         headers: {
//           'Content-type': 'application/json'
//         },
//         body: JSON.stringify(this.state)
//       })
//       .then((result) =>{
//         return result.json()
//       } )
//       .then((info) => { console.log(info); })

//     }

    // render(){
    //   const { classes } = this.props;
    //   const { first_name, pronouns, preferences } = this.state;
    //   return (

        
    //     <form onSubmit={this.handleSubmit}>
    //       <label> First name: 
    //       <input name="firstName" type="text" value={this.state.first_name} onChange={this.handleChange} />
    //       </label>
    //       <br />

    //       <label> Pronouns: 
    //       <input name="pronouns" type="text" value={this.state.pronouns} onChange={this.handleChange} />
    //       </label>
    //       <br />

    //       <label> Preferences: 
    //       <input name="preferences" type="text" value={this.state.preferences} onChange={this.handleChange} />
    //       </label>
    //       <br />
    //       <input type="submit" value="submit" />

    //     </form>
    //   );
    // }
// }

