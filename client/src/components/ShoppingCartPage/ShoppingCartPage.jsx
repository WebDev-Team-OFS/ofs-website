import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './shoppingcart-page.css';

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

    // Function to handle adding or subtracting quantity
    const updateCartItemQuantity = (id, delta) => {
        setCartItems(cartItems.map(item => 
            item.id === id ? { ...item, quantity: Math.max(0, item.quantity + delta) } : item
        ));
    };

    // Function to remove an item from the cart
    const removeItemFromCart = (id) => {
        setCartItems(cartItems.filter(item => item.id !== id));
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
        return { total: total.toFixed(2), deliveryCharge, totalWeight };
    };

    const { total, deliveryCharge, totalWeight } = calculateTotal();

    return (
        <div className="shopping-cart">
            <div className="cart-header">
                <h1>OFS Shopping Cart</h1>
                {totalWeight < 20 && cartItems.length > 0 && (
                    <div>
                        Free Shipping
                        <div className="sub-text">(weight less than 20 lbs)</div>
                    </div>
                )}
            </div>
            <div className="cart-body">
                {cartItems.length > 0 ? (
                    cartItems.map(item => (
                        <div key={item.id} className="cart-item">
                            <div className="item-image">
                                <img src={`./src/img/food/${item.name.toLowerCase().replace(/ /g, '-')}.png`} alt={item.name} />   
                            </div>
                            <div className="item-details">
                                <h2>{item.name} - Weight {item.weight} Lb</h2>
                                <p className="price">${item.price.toFixed(2)} each</p>
                                <div className="quantity-control">
                                    <button onClick={() => updateCartItemQuantity(item.id, -1)} disabled={item.quantity <= 1}>-</button>
                                    <span>{item.quantity}</span>
                                    <button onClick={() => updateCartItemQuantity(item.id, 1)}>+</button>
                                    <button onClick={() => removeItemFromCart(item.id)} className="remove-button">Remove</button>
                                </div>
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