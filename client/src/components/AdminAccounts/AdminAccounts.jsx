import '../AdminProducts/admin-products.css'
import './admin-accounts.css'
import axios from 'axios'
import React, {useState, useEffect } from 'react';
import AdminGroceryCard from '../AdminGroceryCard/AdminGroceryCard'
import ProductForm from '../ProductForm/ProductForm';
import { checkAdminLoginHelper } from '../utils';
import { useNavigate } from 'react-router-dom';


function AdminProducts() {

    const [adminAccounts, setAdminAccounts] = useState([]);

    const navigate = useNavigate();

    const checkLogin = async (e) => {
        if (await checkAdminLoginHelper() == false) {
            navigate('/admin/login')
            console.log("admin login expired")
        }
    }

    const fetchData = async () => {
        try {
            let response = await axios.get(`http://127.0.0.1:8080/api/admin/view_admins`);
            let admins = response.data.admins;
            console.log(admins);
            if (admins) {
                setAdminAccounts(admins);
            }
        }
        catch {
            console.log("ERROR")
        }
        
    }

    const deleteAdmin = async (emp_id) => {
        checkLogin();
        try {
            const response = await axios.delete(`http://127.0.0.1:8080/api/admin/remove_admin/${emp_id}`, {
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("admin_access_token")}`
                },
            });
            fetchData();
        }
        catch (e) {
            console.log(e)
        }
    }

    useEffect(() =>{
        checkLogin();
        fetchData();
    }, [])

    return(
        <div className="admin-page-container">
           <header>
            <h1>OFS Admin Dashboard</h1>
            <div className="admin-page-buttons">
                <button>Products</button>
                <button>Statistics</button>
                <button>Admin Accounts</button>
            </div>
           </header>
           <div className="admin-accounts-body">
            <h1>Admin Accounts</h1>
            <div className="admin-accounts-container">
                {adminAccounts.map((admin) => (
                    <div key={admin.emp_id} className="admin-account">
                        <p>
                            <strong> First Name: </strong> {admin.first_name}
                        </p>
                        <p>
                            <strong> Last Name: </strong> {admin.last_name}
                        </p>
                        <p>
                            <strong> Username: </strong> {admin.username}
                        </p>
                        <p>
                            <strong> Email: </strong> {admin.email}
                        </p>
                        <p>
                            <strong> Account created on </strong> {Date(admin.date_created)}
                        </p>
                        <button className="delete-account-button" onClick={() => deleteAdmin(admin.emp_id)}>DELETE ACCOUNT</button>
                    </div>
                ))
                }
            </div>
           </div>
          
        </div>
    )
}

export default AdminProducts;