import { useState } from 'react'
// dob
const Add = ({onAdd}) => {
    const [firstname, setFirstName] = useState ('')
    const [lastname, setLastName] = useState ('')
    const [pronouns, setPronouns] = useState ('')
    const [preferences, setPreference] = useState ('')
    const [dob, setDob] = useState ('')
    const onSubmit = (e) => {
        e.preventDefault()

    //     onAdd({ name, pronouns, preferences})

        setFirstName('')
        setPronouns('')
        setPreference('')
        setDob('')
    }

    return (
        <form className = 'add-form' onSubmit ={onSubmit}>
            <div className = 'form-control'>
                <label>First Name</label>
                <input type='text' placeholder ='Add first name' 
                value = {firstname} onChange={(e) => setFirstName(e.target.value)}/>
            </div>
            <div className = 'form-control'>
                <label>Last Name</label>
                <input type='text' placeholder ='Add last name' 
                value = {lastname} onChange={(e) => setLastName(e.target.value)}/>
            </div>
            <div className = 'form-control'>
                <label>Pronouns</label>
                <input type='text' placeholder ='Add pronouns' 
                value = {pronouns} onChange={(e) => setPronouns(e.target.value)}/>
            </div>
            <div className = 'form-control'>
                <label>Preferences</label>
                <input type='text' placeholder ='Add preferences' 
                value = {preferences} onChange={(e) => setPreference(e.target.value)}/>
            </div>
            <div className = 'form-control'>
                <label>Date of Birth</label>
                <input type='text' placeholder ='Add Date of Birth' 
                value = {dob} onChange={(e) => setDob(e.target.value)}/>
            </div>
            <input type ='submit' value = 'Submit' 
            className = 'btn btn-block'/>
        </form>
    )
}

export default Add