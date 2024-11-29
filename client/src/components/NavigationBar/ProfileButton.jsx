import React from 'react'
import { useState, useEffect } from 'react'
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function ProfileButton() {
    const [profileOptions, setProfileOptions] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const navigate = useNavigate();
    
    const checkLogin = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8080/api/protected', {
                withCredentials: true  // Ensures cookies (including session cookies) are sent with the request
            });
            setIsLoggedIn(true);
            console.log("logged in");
        }
        catch (error) {
            setIsLoggedIn(false);
            console.log("not logged in");
            console.error("Error response:", error.response);
            console.log(error.response.data);
        }
        // setIsLoggedIn(true);
    }

    const clickProfile = () => {
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
            setIsLoggedIn(false);
            setProfileOptions(false);
            console.log(response.data);
            window.location.reload();

        }
        catch (error) {
            console.log(error.response);
        }
        finally {
            setProfileOptions(false);
            console.log("final");
        }
         
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
                        <p>View Profile</p>
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