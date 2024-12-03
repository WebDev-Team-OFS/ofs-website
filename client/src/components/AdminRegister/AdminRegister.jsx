
import './admin-register.css'
import axios from 'axios'
import React, {useState, useEffect } from 'react';
import AdminGroceryCard from '../AdminGroceryCard/AdminGroceryCard'
import ProductForm from '../ProductForm/ProductForm';
import { checkAdminLoginHelper } from '../utils';
import { useNavigate } from 'react-router-dom';


function AdminRegister({onCancel}) {

    

    const [formData, setFormData] = useState({
        email: "",
        first_name: "",
        last_name: "",
        username: "",
        password: "",
        confirm_password: "",
    })

    const navigate = useNavigate();

    const checkLogin = async (e) => {
        if (await checkAdminLoginHelper() == false) {
            navigate('/admin/login')
            console.log("admin login expired")
        }
    }

    const handleInputChange = (e) => {
        const { name, value } = e.target; // Get the name and value of the input field
        setFormData((prev) => ({
          ...prev, // Spread the previous form data
          [name]: value,   // Update the specific field that was changed
        }));
      };

    const handleSubmit = async (e) => {
        e.preventDefault();
        checkLogin();
        try {
            console.log(formData);
            const response = await axios.post('http://127.0.0.1:8080/api/admin/add_admin', JSON.stringify(formData), {
                headers: {
                    'Content-Type': 'application/json', 
                    "Authorization": `Bearer ${localStorage.getItem("admin_access_token")}`
                },
            });
            console.log("admin added");
            onCancel();
            window.location.reload();
        }
        catch (e) {
            console.log(e)
        }
       
    }

    return(
        <div className="admin-register-container">
            <form className="admin-register-form">
                <h1>Create new admin</h1>
                <div className="input-wrapper">
                    <label className="email">Email address</label>
                    <input
                    type="email"
                    name="email"
                    required
                    value={formData.email}
                    onChange={handleInputChange}
                    placeholder="Enter your email"
                    />
                </div>
                <div className="input-row">
                    <div className="input-wrapper">
                        <label className="first_name">First Name</label>
                        <input
                        type="text"
                        name="first_name"
                        required
                        value={formData.first_name}
                        onChange={handleInputChange}
                        placeholder="First name"
                        />
                    </div>
                    <div className="input-wrapper">
                        <label className="last_name">Last Name</label>
                        <input
                        type="text"
                        name="last_name"
                        required
                        value={formData.last_name}
                        onChange={handleInputChange}
                        placeholder="Last name"
                        />
                    </div>
                </div>
                <div className="input-wrapper">
                    <label className="username">Username</label>
                    <input
                    type="text"
                    name="username"
                    required
                    value={formData.username}
                    onChange={handleInputChange}
                    placeholder="Choose a username"
                    />
                </div>
                <div className="input-wrapper">
                    <label className="password">Password</label>
                    <input
                    type="password"
                    name="password"
                    required
                    value={formData.password}
                    onChange={handleInputChange}
                    placeholder="Enter your password"
                    />
                </div>
                <div className="input-wrapper">
                    <label className="confirm_password">Confirm Password</label>
                    <input
                    type="password"
                    name="confirm_password"
                    required
                    value={formData.confirm_password}
                    onChange={handleInputChange}
                    placeholder="Confirm your password"
                    />
                </div>
                <button className="create-admin-button" onClick={handleSubmit}>Create Admin</button>
            </form>
        </div>
          
    )
}

export default AdminRegister;