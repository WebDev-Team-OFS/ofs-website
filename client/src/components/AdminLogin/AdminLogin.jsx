import React from 'react'
import "./admin-login.css"
import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { checkAdminLoginHelper } from '../utils';


export default function AdminLogin() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const navigate = useNavigate();

    const checkLogin = async (e) => {
        if (await checkAdminLoginHelper()) {
            navigate('/admin/products')
            console.log("admin logged in!")
        }
    }

    const submitLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(`http://127.0.0.1:8080/api/admin/login`, {
                email,
                password,
            }, { withCredentials: true });
            if (response.data) {
                localStorage.setItem('admin_access_token', response.data.access_token);
                localStorage.setItem('admin_refresh_token', response.data.refresh_token);
                console.log("login successful")
              }
            navigate(`/admin/products`);
            
        }
        catch (error) {
            console.log(error.response ? error.response.data : error.message);
            setError("The email or password is incorrect")
        }
      

    }

    useEffect(() => {
        checkLogin();
    }, [])

  return (
    <div className="admin-login-wrapper">
        <form className="admin-login" action="" onSubmit={submitLogin}>
            <h1>OFS Admin Dashboard</h1>
            <div className="input-wrapper">
                <label htmlFor="email">Email</label>
                <input type="email" id="email" name="email" onChange={(e) => setEmail(e.target.value)} />
            </div>
            <div className="input-wrapper">
                <label htmlFor="password">Password</label>
                <input type="password" id="password" name="password" onChange={(e) => setPassword(e.target.value)} />
                <label className="error" htmlFor="error">{error}</label>
            </div>
            <button type="submit">Log in</button>
        </form>
    </div>
    
   
  )
}
