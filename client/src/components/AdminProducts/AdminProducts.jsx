import './admin-products.css'
import axios from 'axios'
import React, {useState, useEffect } from 'react';
import AdminGroceryCard from '../AdminGroceryCard/AdminGroceryCard'
import ProductForm from '../ProductForm/ProductForm';
import { checkAdminLoginHelper } from '../utils';
import { useNavigate, useLocation } from 'react-router-dom';


function AdminProducts() {

    const [products, setProducts] = useState([]);
    const [showProductForm, setShowProductForm] = useState(false);
   

    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const query = queryParams.get('q');
    const [input, setInput] = useState(() => {
        if (query) {
            return query;
        }
        else {
            return "";
        }
    });
    const navigate = useNavigate();

    const checkLogin = async (e) => {
        if (await checkAdminLoginHelper() == false) {
            navigate('/admin/login')
            console.log("admin login expired")
        }
    }

    const fetchData = async () => {
        let response = null;
        if (query) {
            response = await axios.get(`http://127.0.0.1:8080/api/search?q=${query}`);
        }
        else {
            response = await axios.get(`http://127.0.0.1:8080/api/search?q=`);
        }
       
        console.log(query);
        let products = response.data.products;
        if (products) {
            setProducts(products);
        }
        
    }

    const handleCancel = async (e) => {
        checkLogin();
        setShowProductForm(false);
       
    };

    const AddProduct = async (e) => {
        checkLogin();
        setShowProductForm(true)
    }

    const handleSearch = async (event) => {
        if (event.key == "Enter") {
            navigate(`/admin/products?q=${input}`)
        }
    }

    const handleLogOut = () => {
        localStorage.removeItem("admin_access_token");
        localStorage.removeItem("admin_refresh_token");
        navigate(`/admin/login`)
    }

    useEffect(() =>{
        checkLogin();
        fetchData();
    }, [query])

    return(
        <div className="admin-page-container">
            {showProductForm ? 
                (
                    <>
                        <ProductForm product={null} onCancel={handleCancel}  / > 
                        <div className="black-cover" onClick={handleCancel}></div>
                    </>
                
                
                ): <></>}
           <header>
            <h1>OFS Admin Dashboard</h1>
            <div className="admin-page-buttons">
                <button onClick={() => navigate("/admin/products")}>Products</button>
                <button onClick={() => navigate("/admin/accounts")}>Admin Accounts</button>
                <button onClick={handleLogOut}>Log Out</button>
            </div>
           </header>
           <div className="admin-products-body">
            <h1>OFS Products</h1>
           <input type="text" className="admin-product-search" value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={handleSearch}/>
           <button className="add-product-button" onClick={AddProduct}>Add Product</button>
            <div className="admin-products-container">
                
                    {products.length > 0 ? (
                        products.map(product => (
                            <AdminGroceryCard 
                                key = {product.id}
                                product ={product}
                            />
                        ))
                    ) : (
                        <p>No products found.</p> 
                    )}
            </div>
           </div>
          
        </div>
    )
}

export default AdminProducts;