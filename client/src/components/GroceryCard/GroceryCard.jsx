import './grocery-card.css'
import { useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';


function GroceryCard({product}) {
    const navigate = useNavigate();
    const [outOfStock, setOutOfStock] = useState(false);

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

    const addToCart = () => {
        console.log("CART!!")
        let cart = JSON.parse(localStorage.getItem("cart")) || [];
        
        let cartProduct = cart.find(grocery => grocery.product_id === product.product_id);

        if (cartProduct) {
            cartProduct.quantity++;
        }
        else {
            cart.push({ product_id: product.product_id, quantity: 1 });
        }
        console.log(cart);
        
        localStorage.setItem("cart", JSON.stringify(cart));
    }

    return(
        <>
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