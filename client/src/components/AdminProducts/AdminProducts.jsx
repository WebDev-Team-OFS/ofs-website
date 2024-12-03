import './admin-products.css'
import axios from 'axios'
import React, {useState, useEffect } from 'react';
import AdminGroceryCard from '../AdminGroceryCard/AdminGroceryCard'
import ProductForm from '../ProductForm/ProductForm';


function AdminProducts() {

    const [products, setProducts] = useState([]);

    const fetchData = async () => {
        let response = await axios.get(`http://127.0.0.1:8080/api/search?q=`);
        let products = response.data.products;
        if (products) {
            setProducts(products);
        }
        
    }

    useEffect(() =>{
        fetchData();
    }, [])

    return(
        <div className="admin-page-container">
            {/* {products.length > 0 ? <ProductForm product = {products[0]} /> : <></>} */}
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