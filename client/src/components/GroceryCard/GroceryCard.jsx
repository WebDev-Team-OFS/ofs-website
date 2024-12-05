import './grocery-card.css'
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { checkLoginHelper} from '../utils'
import axios from 'axios'
import PopUp from '../PopUp/PopUp'


function GroceryCard({product}) {
    const navigate = useNavigate();
    const [outOfStock, setOutOfStock] = useState(false);
    const [showPopUp, setShowPopUp] = useState(false);

    const goToProduct = (event) => {
        if (!event.target.classList.contains("add-to-cart-button")) {
            navigate(`/product/${product.product_id}`);
        }
    }

    const checkStock = () => {
        if (product.stock <=0) {
            setOutOfStock(true);
        }
        else {
            setOutOfStock(false);
        }
    }

    useEffect(() => {
        checkStock();
    }, [])

    const addToCart = async () => {
        if (await checkLoginHelper()) {
            try {
                const response = await axios.post('http://127.0.0.1:8080/api/add_to_cart', {product_id: product.product_id, quantity: 1}, {
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("access_token")}`
                    }  
                })
            }
            catch (e) {
            }
        }
        else {
            setShowPopUp(true);
        }
        
    }

    return(
        <>
            {showPopUp ? <PopUp text="Log in to add to your cart" closePopUp={() => setShowPopUp(false)} /> : <></>}
            <div className="grocery-card" onClick={goToProduct}>
                <img src={`http://127.0.0.1:8080/api/image/${product.product_id}`} alt="" />
                <div>
                    <p className="price">${product.price}</p>
                    <p className="title">{product.brand + " " + product.name}</p>
                    <p className="weight">{product.weight} lbs</p>
                </div>
                {
                    outOfStock ? (
                        <>
                            <button className="out-of-stock add-to-cart-button">OUT OF STOCK</button>
                        </>

                       

                    ) :
                    (
                        <button onClick={addToCart} className="add-to-cart-button">ADD TO CART</button>
                    )
                }
                
            </div>
        </>
    )
}

export default GroceryCard