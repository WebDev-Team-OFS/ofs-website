import './admin-grocery-card.css'
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import ProductForm from '../ProductForm/ProductForm';
import { checkAdminLoginHelper } from '../utils';


function AdminGroceryCard({product}) {
    
    const [showProductForm, setShowProductForm] = useState(false);

    const navigate = useNavigate()

    const checkLogin = async (e) => {
        if (await checkAdminLoginHelper() == false) {
            navigate('/admin/login')
            console.log("admin login expired");
        }
    }

    const handleEdit = async () => {
        checkLogin();
        setShowProductForm(true)
    }

    const handleCancel = async (e) => {
        checkLogin();
        setShowProductForm(false);
       
    };

    

    return(
        <>
            {showProductForm ? 
                (
                    <>
                        <ProductForm product={product} onCancel={handleCancel}  / > 
                        <div className="black-cover" onClick={handleCancel}>TEST</div>
                    </>
                
                
                ): <></>}
            <div className="grocery-card">
                <img src={`http://127.0.0.1:8080/api/image/${product.product_id}`} alt="" />
                <div>
                    <p className="price">${product.price}</p>
                    <p className="title">{product.brand + " " + product.name}</p>
                    <p className="weight">{product.weight} lbs</p>
                </div>
                    <button  className="add-to-cart-button" onClick={handleEdit}>EDIT</button>
            </div>
        </>
    )
}

export default AdminGroceryCard