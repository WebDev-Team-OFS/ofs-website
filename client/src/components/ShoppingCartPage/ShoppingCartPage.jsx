import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './shoppingcart-page.css';
import axios from 'axios';
import { checkLoginHelper } from '../utils';
import PopUp from '../PopUp/PopUp';


function ShoppingCartPage() {
    const navigate = useNavigate();

    // Define initial cart items
    //For Pictures to show up it, needs to have same name as png ex. Almond Milk almond-milk.png, Lunchly lunchly.png, Heavy Cream heavy-cream.png
    const initialCartItems = [
        { id: 1, name: 'Signature Farms Whole Turkey', price: 19.14, weight: 12, quantity: 1 },
        { id: 2, name: 'Eggs', price: 6.99, weight: 1.5, quantity: 2 },
        { id: 3, name: 'Almond Milk', price: 6.99, weight: 1.5, quantity: 2 }
    ];

    // State for cart items
    const [cartItems, setCartItems] = useState([]);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [showPopUp, setShowPopUp] = useState(false);

    const getCart = async () => {
        let cart = []
        let tempCart = []
        if (await checkLoginHelper()) {
            try {
                const response = await axios.get('http://127.0.0.1:8080/api/view_cart', {
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("access_token")}`
                    }  
                });
                console.log("GET DB CART");
                console.log(response.data.cart)
                tempCart = response.data.cart;
            }
            catch {
                console.log("DID NOT GET THE DB CART")
            }

        }
        for (let i = 0; i < tempCart.length; i++) {
            console.log(tempCart[i].product_id)
            try{
                let response = await axios.get(`http://127.0.0.1:8080/api/product/${tempCart[i].product_id}`);
                    
                response.data.product.quantity = tempCart[i].quantity;
                console.log(response.data.product);
                cart.push(response.data.product);
            }
            catch (error) {
                console.log(error);
            }        
        }
        console.log(cart);
        setCartItems(cart);
    }


    const goToCheckOut = async () => {
        if (await checkLoginHelper()) {
            navigate('/checkout');
        }
        else {
            setShowPopUp(true);
        }
    }

    useEffect(() => {
        getCart();
    }, [])

    // Function to handle adding or subtracting quantity
    const updateCartItemQuantity = async (id, delta) => {
       

        let currentItem = cartItems.find(item => item.product_id === id);
        let currentQuantity = currentItem.quantity;
        

        if (await checkLoginHelper()) {
            try {
                const response = await axios.put(`http://127.0.0.1:8080/api/update_cart_item`, {product_id: id, quantity: currentQuantity + delta}, {
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("access_token")}`
                    }  
                });
                setCartItems(cartItems.map(item => 
                    item.product_id === id ? { ...item, quantity: Math.max(0, item.quantity + delta) } : item
                ));
                console.log("REMOVE FROM DB CART");
            }
            catch {
                console.log("DID NOT REMOVE FROM THE DB CART")
            }

        }
        else {
            setShowPopUp(true)
        }
    };

    // Function to remove an item from the cart
    const removeItemFromCart = async (id) => {
        if (await checkLoginHelper()) {
            try {
                const response = await axios.delete(`http://127.0.0.1:8080/api/remove_from_cart/${id}`, {
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("access_token")}`
                    }  
                });
                setCartItems(cartItems.filter(item => item.product_id !== id));
                console.log("REMOVE FROM DB CART");
            }
            catch {
                console.log("DID NOT REMOVE FROM THE DB CART")
            }
        }
        else {
           setShowPopUp(true)
        }
    };

    // Calculate total price and weight
    const calculateTotal = () => {
        let total = 0;
        let totalWeight = 0;
        cartItems.forEach(item => {
            total += item.price * item.quantity;
            totalWeight += item.weight * item.quantity;
        });
        const deliveryCharge = totalWeight > 20 ? 5 : 0;
        return { total: total.toFixed(2), deliveryCharge, totalWeight: totalWeight.toFixed(2) }; //CHECK
    };

    const { total, deliveryCharge, totalWeight } = calculateTotal();

    return (
        <div className="shopping-cart">
            {showPopUp ? <PopUp text="Your login has expired. Refresh" closePopUp={() => setShowPopUp(false)} /> : <></>}
            <div className="cart-header">
                <h1>OFS Shopping Cart</h1>
            </div>
            <div className="cart-body">
                {cartItems.length > 0 ? (
                    cartItems.map(item => (
                        <div key={item.product_id} className="cart-item">
                            <div className="item-image">
                                <img src={`http://127.0.0.1:8080/api/image/${item.product_id}`} alt={item.name} />   
                            </div>
                            <div className="item-details">
                                <h2>{item.brand + " " + item.name}</h2>
                                <p className="price">${item.price} each</p>
                                <p className="weight">{item.weight} lbs each</p>
                                <div className="quantity-control">
                                    <button onClick={() => updateCartItemQuantity(item.product_id, -1)} disabled={item.quantity <= 1} className="quantity-button">-</button>
                                    <span>{item.quantity}</span>
                                    <button onClick={() => updateCartItemQuantity(item.product_id, 1)} className="quantity-button">+</button>
                                    <button onClick={() => removeItemFromCart(item.product_id)} className="remove-button">Remove</button>
                                </div>
                            </div>
                            <div className="item-totals">
                                <p className="total-price">${(item.price * item.quantity).toFixed(2)}</p>
                                <p className="total-weight">{(item.weight * item.quantity).toFixed(2)} lbs</p>
                            </div>
                        </div>
                    ))
                ) : (
                    <p>There is nothing in the cart.</p>
                )}
            </div>
            {cartItems.length > 0 ? (
                <div className="cart-footer">
                    <div className="subtotal">
                        <h2>Est. Subtotal: ${total}</h2>
                        <p>Total Weight: {totalWeight} lbs</p>
                        {deliveryCharge > 0 && 
                        <p>*A shipping fee of ${deliveryCharge}.00 is added to deliveries over 20 pounds</p>
                        }
                    </div>
                    <button className="checkout-button" onClick={goToCheckOut}>
                        Checkout
                    </button>
                </div>
            ) : null}
        </div>
    );
}

export default ShoppingCartPage;