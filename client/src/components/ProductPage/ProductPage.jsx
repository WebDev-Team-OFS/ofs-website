import './product-page.css'
import { useParams } from 'react-router-dom'
import {useEffect, useState} from 'react'
import axios from 'axios'
import { checkLoginHelper } from '../utils'
import PopUp from '../PopUp/PopUp'




function ProductPage() {

    const [product, setProduct] = useState({});
    const [itemQuantity, setItemQuantity] = useState(1);
    const [isSuccess, setIsSuccess] = useState(false);
    const [showPopUp, setShowPopUp] = useState(false);

    const param = useParams();
    const id = param.id;

    const fetchData = async () => {
        let response = await axios.get(`http://127.0.0.1:8080/api/product/${id}`); 
        setProduct(response.data.product);
    }


    const addToCart = async () => {
        if (await checkLoginHelper()) {
            try {
                const response = await axios.post('http://127.0.0.1:8080/api/add_to_cart', {product_id: product.product_id, quantity: itemQuantity}, {
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("access_token")}`
                    }  
                });
                setIsSuccess(true);
            }
            catch {
            }
        }
        else {
            setShowPopUp(true)
            setIsSuccess(false);
        }
        

    }

    useEffect(() => {
        fetchData();
    }, [])

    return (
        <>
            {showPopUp ? <PopUp text="Log in to add items to your cart" closePopUp={() => setShowPopUp(false)} /> : <></>}
            <div className="product-page-container">
                <div className="product-image-container">
                    <img src={`http://127.0.0.1:8080/api/image/${product.product_id}`} alt="" />
                </div>
                <div className="product-content">
                    <h1 className="product-title">{product.brand + " " + product.name}</h1>
                    <div className="price-weight">
                        <p className="product-price">${product.price}</p>
                        <p className="product-weight">{product.weight} lbs</p>
                    </div>
                    <p className="product-description">
                        {product.description}
                    </p>
                    <div className="quantity-control">
                        <button onClick={() => setItemQuantity(itemQuantity-1)} disabled={itemQuantity <= 1} className="quantity-button">-</button>
                        <span>{itemQuantity}</span>
                        <button onClick={() => setItemQuantity(itemQuantity+1)} className="quantity-button">+</button>
                     </div>
                    <button className="add-to-cart" onClick={addToCart}>ADD TO CART</button>
                    {
                        isSuccess ? 
                        <p className="success">You have added the item to your cart</p> : <></>
                    }
                </div>
            </div>
        </>
    )
}


export default ProductPage