import './product-page.css'
import { useLocation, useParams } from 'react-router-dom'
import {useEffect, useState} from 'react'
import axios from 'axios'




function ProductPage() {

    const [product, setProduct] = useState({});
    const [itemQuantity, setItemQuantity] = useState(1);
    const [isSuccess, setIsSuccess] = useState(false);

    const param = useParams();
    const id = param.id;

    const fetchData = async () => {
        console.log("fetch data");
        let response = await axios.get(`http://127.0.0.1:8080/api/product/${id}`); 
        console.log(response.data.product);
        setProduct(response.data.product);
    }


    const addToCart = () => {
        let cart = JSON.parse(localStorage.getItem("cart")) || [];
        
        let cartProduct = cart.find(grocery => grocery.product_id === product.product_id);

        if (cartProduct) {
            cartProduct.quantity += itemQuantity;
        }
        else {
            cart.push({ product_id: product.product_id, quantity: itemQuantity });
        }        
        localStorage.setItem("cart", JSON.stringify(cart));
        setIsSuccess(true);

    }

    useEffect(() => {
        fetchData();
    }, [])

    return (
        <>
            <div className="product-page-container">
                <div className="product-image-container">
                    <img src={product.imageURL} alt="" />
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

{/* <GroceryCard price ="7.99" title="Pavesi Gocciole Chocolate Chip Cookies" weight="1.00" imageURL="./src/img/food/cookies.png" /> */}


export default ProductPage