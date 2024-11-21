import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './shoppingcart-page.css';
import axios from 'axios';


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
    const [cartItems, setCartItems] = useState(initialCartItems);
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    const getCart = async () => {
        let cart = []
        if (isLoggedIn) {

        }
        else {
            const localStorageCart = JSON.parse(localStorage.getItem("cart")) || [];

            for (let i = 0; i < localStorageCart.length; i++) {
                console.log(localStorageCart[i].product_id)
                try{
                    let response = await axios.get(`http://127.0.0.1:8080/api/product/${localStorageCart[i].product_id}`);
                    
                    response.data.product.quantity = localStorageCart[i].quantity;
                    console.log(response.data.product);
                    cart.push(response.data.product);
                }
                catch (error) {
                    console.log(error);
                }
                
            }
        }
        console.log(cart);
        setCartItems(cart);
    }

    useEffect(() => {
        getCart();
    }, [])

    // Function to handle adding or subtracting quantity
    const updateCartItemQuantity = (id, delta) => {
        setCartItems(cartItems.map(item => 
            item.product_id === id ? { ...item, quantity: Math.max(0, item.quantity + delta) } : item
        ));

        if (isLoggedIn) {
           
        }
        else {
            let localStorageCart = JSON.parse(localStorage.getItem("cart")) || [];
            localStorageCart = localStorageCart.map(item => item.product_id === id ? { ...item, quantity: Math.max(0, item.quantity + delta) } : item);
            localStorage.setItem("cart", JSON.stringify(localStorageCart));
        }
    };

    // Function to remove an item from the cart
    const removeItemFromCart = (id) => {
        setCartItems(cartItems.filter(item => item.product_id !== id));
        
        if (isLoggedIn) {

        }
        else {
            let localStorageCart = JSON.parse(localStorage.getItem("cart")) || [];
            localStorageCart = localStorageCart.filter(item => item.product_id !== id);
            localStorage.setItem("cart", JSON.stringify(localStorageCart));
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
            <div className="cart-header">
                <h1>OFS Shopping Cart</h1>
                {totalWeight < 20 && cartItems.length > 0 && (
                    <p>
                        *Qualifies for free shipping (under 20 lbs)
                    </p>
                )}
            </div>
            <div className="cart-body">
                {cartItems.length > 0 ? (
                    cartItems.map(item => (
                        <div key={item.product_id} className="cart-item">
                            <div className="item-image">
                                <img src=/*{`./src/img/food/${item.name.toLowerCase().replace(/ /g, '-')}.png`}*/"" alt={item.name} />   
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
                        {deliveryCharge > 0 && <p>Delivery Charge: ${deliveryCharge}</p>}
                    </div>
                    <button className="checkout-button" onClick={() => navigate('/checkout')}>
                        Checkout
                    </button>
                </div>
            ) : null}
        </div>
    );
}

export default ShoppingCartPage;