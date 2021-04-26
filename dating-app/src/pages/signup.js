import React from 'react';
import {useState, useEffect } from 'react'
import {Nav,NavLink,Bars,NavMenu,NavBtn,NavBtnLink} from '../Components/Navbar/NavbarElements'
// export const Users = ({ users }) => { return (<div>{movies.length}</div> ) }

const Signup = () => {
  const [showAddTask, setShowAddTask] = useState (false)
  const [info, setTasks] = useState([])
  useEffect (() => {
    const getTasks = async () => {
      const tasksFromServer = await fetchTasks() 
      setTasks(tasksFromServer)
    }
    getTasks()
  }, [])

  const fetchTasks = async() => {
    const rest = await fetch ('http://localhost:5000/authspotify')
    const data = await rest.text()
  
    return data
  }

  const add = async(task) => {
    const res = await fetch('http://localhost:5000/add', {
      method: 'POST',
      headers: {
      'Content-type': 'application/json'
      },
      body: JSON.stringify(task)
    })

    const data = await  res.json()
    setTasks([...info, data])


    // const id = Math.floor(Math.random() * 10000) + 1 
    // const newTask = { id, ...task}
    // setTasks([...tasks, newTask])
  }
  return (
    <div className="container">
        <button onClick={async () => {await fetchTasks("Example");}}>Sign Up</button>
    </div>
    // <html>
    //   <head>
    //     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.2/css/bulma.min.css" />
    //   </head>
    //   <body>
    //     <section class="hero is-primary is-fullheight">
    //       <div class="hero-body">
    //         <div class="container has-text-centered">
               
    //         <h1 class="title">
    //           Music Match
    //         </h1>
    //         <h2 class="subtitle">
    //           Let your music play matchmaker today. 
    //         </h2>

    //           <div class="column is-4 is-offset-4">

    //             <form method="GET" action="http://localhost:5000/authspotify">
    //               <button class="button is-block is-info is-large is-fullwidth">Sign Up With Spotify</button>
    //             </form>
    //           </div>
    //         </div>
    //       </div>
    //     </section>
    //   </body>
    // </html>
  );
};

export default Signup;