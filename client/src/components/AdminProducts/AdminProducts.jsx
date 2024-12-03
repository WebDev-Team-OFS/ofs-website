import './admin-products.css'
import axios from 'axios'
import React, {useState, useEffect } from 'react';
import AdminGroceryCard from '../AdminGroceryCard/AdminGroceryCard'
import ProductForm from '../ProductForm/ProductForm';
import { checkAdminLoginHelper } from '../utils';
import { useNavigate } from 'react-router-dom';


function AdminProducts() {

    const [products, setProducts] = useState([]);
    const [showProductForm, setShowProductForm] = useState(false);

    const navigate = useNavigate();

    const checkLogin = async (e) => {
        if (await checkAdminLoginHelper() == false) {
            navigate('/admin/login')
            console.log("admin login expired")
        }
    }

    const fetchData = async () => {
        let response = await axios.get(`http://127.0.0.1:8080/api/search?q=`);
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

    useEffect(() =>{
        checkLogin();
        fetchData();
    }, [])

    return(
        <div className="admin-page-container">
            {showProductForm ? 
                (
                    <>
                        <ProductForm product={null} onCancel={handleCancel}  / > 
                        <div className="black-cover" onClick={handleCancel}>TEST</div>
                    </>
                
                
                ): <></>}
           <header>
            <h1>OFS Admin Dashboard</h1>
            <div className="admin-page-buttons">
                <button>Products</button>
                <button>Statistics</button>
                <button>Admin Accounts</button>
            </div>
           </header>
           <div className="admin-products-body">
            <h1>OFS Products</h1>
           <input type="text" className="admin-product-search" />
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