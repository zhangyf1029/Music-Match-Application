import React from 'react'
import {Nav,NavLink,Bars,NavMenu,NavBtn,NavBtnLink} from './NavbarElements'
const Navbar = () => {
    return (
        <>
            <Nav>
                <NavLink to = "/">
                    <img src={require('../../images/logo.svg')} alt='logo' />
                </NavLink>
                <Bars />
                <NavMenu>
                    <NavLink to = "/about" activeStyle>
                        About
                    </NavLink>
                    <NavLink to = "/match" activeStyle>
                        Start Matching
                    </NavLink>
                    <NavLink to = "/contact" activeStyle>
                        Contact Us
                    </NavLink>
                    <NavLink to = "/signup" activeStyle>
                        Sign Up
                    </NavLink>
                    <NavBtnLink to ="/signin"> Sign In </NavBtnLink>
                </NavMenu>
            </Nav>
            
        </>
    )
}

export default Navbar
