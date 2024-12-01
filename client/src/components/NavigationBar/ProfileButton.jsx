import React from 'react'
import { useState, useEffect } from 'react'
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { checkLoginHelper } from '../utils'

function ProfileButton() {
    const [profileOptions, setProfileOptions] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const navigate = useNavigate();
    
   const checkLogin = async () => {

        if (await checkLoginHelper() == true) {
            setIsLoggedIn(true)
            console.log('TRUE!!! DUBS')
        }
        else if (await checkLoginHelper() == false) {
            console.log("HI!!")
            setIsLoggedIn(false)
        }
        else {
            console.log("WHT AM I HERE?")
        }
   }

    const clickProfile = async () => {
        if (profileOptions == true) {
            setProfileOptions(false);
        }
        else {
            setProfileOptions(true);
        }
        
    }

    const handleRegisterButton = () => {
        navigate(`/login`);
    }

    const handleLogOutButton = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:8080/api/logout', {
                withCredentials: true
            });
            localStorage.clear();
            setIsLoggedIn(false);
            setProfileOptions(false);
            console.log(response.data);
        }
        catch (error) {
            console.log(error.response);
        }
        finally {
            setProfileOptions(false);
            navigate(`/`);
            console.log("final");
        }
         
    }

    const goToProfile = async () => {
        if (await checkLoginHelper()) {
            navigate('/profile')
        }
        else {
            console.log("no logged in")
        }
        setProfileOptions(false);
    }

    useEffect(() => {
        checkLogin();
    })

  return (


    <>
         <img className="profile-icon" src="./src/img/profile-icon.png" alt="" onClick={clickProfile}/>
        {profileOptions && (
            <div className="profile-options">
            {
                isLoggedIn && (
                    <>
                        <p onClick={goToProfile}>View Profile</p>
                        <p className="end" onClick={handleLogOutButton}>Logout</p>
                    </>
                )
            }
            {
                !isLoggedIn && (
                    <>
                        <p className="end" onClick={handleRegisterButton}>Sign In/Register</p>
                    </>
                )
            }
            
         </div>
        )}
       
    </>
   
       
  )
}

export default ProfileButton