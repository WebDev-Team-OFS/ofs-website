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
        }
        else if (await checkLoginHelper() == false) {
            setIsLoggedIn(false)
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
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            setIsLoggedIn(false);
            setProfileOptions(false);
        }
        catch (error) {
        }
        finally {
            setProfileOptions(false);
            navigate(`/`);
            window.location.reload();
        }
         
    }

    const goToProfile = async () => {
        if (await checkLoginHelper()) {
            navigate('/profile')
        }
        else {
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