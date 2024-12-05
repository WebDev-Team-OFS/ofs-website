import '../AdminProducts/admin-products.css'
import './admin-accounts.css'
import axios from 'axios'
import React, {useState, useEffect } from 'react';
import { checkAdminLoginHelper } from '../utils';
import { useNavigate } from 'react-router-dom';
import AdminRegister from '../AdminRegister/AdminRegister';


function AdminProducts() {

    const [adminAccounts, setAdminAccounts] = useState([]);
    const [showAdminRegister, setShowAdminRegister] = useState(false);

    const navigate = useNavigate();

    const checkLogin = async (e) => {
        if (await checkAdminLoginHelper() == false) {
            navigate('/admin/login')
        }
    }

    const fetchData = async () => {
        try {
            let response = await axios.get(`http://127.0.0.1:8080/api/admin/view_admins`, {headers: {
                "Authorization": `Bearer ${localStorage.getItem("admin_access_token")}`
            },});
            let admins = response.data.admins;
            if (admins) {
                setAdminAccounts(admins);
            }
        }
        catch (e) {
            console.log(e)
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


    const handleAddAdmin = async () =>{
        checkLogin();
        setShowAdminRegister(true)
    }

    const handleLogOut = () => {
        localStorage.removeItem("admin_access_token");
        localStorage.removeItem("admin_refresh_token");
        navigate(`/admin/login`)
    }

    useEffect(() =>{
        checkLogin();
        fetchData();
    }, [])

    return(
        <div className="admin-page-container">
            {showAdminRegister ? (
                <>
                    <AdminRegister onCancel={() => {setShowAdminRegister(false)}} />
                    <div className="background-shadow" onClick={() => {setShowAdminRegister(false)}}></div>
                </>
            ) : <></>}
           <header>
            <h1 >OFS Admin Dashboard</h1>
            <div className="admin-page-buttons">
                <button onClick={() => navigate("/admin/products")}>Products</button>
                <button onClick={() => navigate("/admin/accounts")}>Admin Accounts</button>
                <button onClick={handleLogOut}>Log Out</button>
            </div>
           </header>
           <div className="admin-accounts-body">
            <h1>Admin Accounts</h1>
            <button className="add-admin-button" onClick={handleAddAdmin}>ADD NEW ADMIN</button>
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
                        <button className="delete-account-button" onClick={() => deleteAdmin(admin.emp_id)} disabled={adminAccounts.length <=1}>DELETE ACCOUNT</button>
                    </div>
                ))
                }
            </div>
           </div>
          
        </div>
    )
}

export default AdminProducts;