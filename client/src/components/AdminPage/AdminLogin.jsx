import React from 'react'
import "./admin-login.css"

export default function AdminLogin() {
  return (
    <div className="admin-login-wrapper">
        <form className="admin-login" action="">
            <h1>OFS Admin Dashboard</h1>
            <div className="input-wrapper">
                <label htmlFor="email">Email</label>
                <input type="email" id="email" name="email" required />
            </div>
            <div className="input-wrapper">
                <label htmlFor="password">Password</label>
                <input type="password" id="password" name="password" required />
            </div>
            <button type="submit">Log in</button>
        </form>
    </div>
    
   
  )
}
