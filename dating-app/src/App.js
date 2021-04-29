import React, { useEffect, useState } from 'react'; //, { useState, useEffect } from 'react';
import HandleSubmit from './Components/HandleSubmit'
import Navbar from './Components/Navbar/index'
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'
import Home from './pages'
import About from './pages/about'
import Contact from './pages/contact'
import Form from './pages/form'
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

  return (
    <html>
      <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.2/css/bulma.min.css" />
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
        </Router>
       </body>
     </html>
  );
}

export default SignUpForm;