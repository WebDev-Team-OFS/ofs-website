import NavigationBar from '../NavigationBar/NavigationBar';
import React, { useState, useEffect } from 'react';
import './checkout-page.css'; // Link to your CSS file for styling
import axios from 'axios';

function CheckoutPage() {
  const [cartItems, setCartItems] = useState([
    { id: 1, name: "Kirkland Large Farm Eggs", price: 8.99, quantity: 1, weight: 1.25 },
    { id: 2, name: "Loaf of Nature's Whole Wheat Bread", price: 13.99, quantity: 1, weight: 1.25 },
    { id: 3, name: "Lunchly", price: 5.99, quantity: 5, weight: 2.5 }
  ]);

  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const getCart = async () => {
    console.log("GETTING CART");
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

  const [deliveryDetails, setDeliveryDetails] = useState({
    address: '',
    city: '',
    zip: ''
  });

  const [paymentDetails, setPaymentDetails] = useState({
    cardName: '',
    cardNumber: '',
    expiryDate: '',
    cvv: ''
  });

  // Total Price Calculation
  const totalPrice = cartItems.reduce((total, item) => total + item.price * item.quantity, 0);
  const totalWeight = cartItems.reduce((total, item) => total + item.weight * item.quantity, 0);

  // Handle input changes
  const handleInputChange = (event, section) => {
    const { name, value } = event.target;
    if (section === "delivery") {
      setDeliveryDetails({ ...deliveryDetails, [name]: value });
    } else if (section === "payment") {
      setPaymentDetails({ ...paymentDetails, [name]: value });
    }
  };

  // Form submission handler
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log('Order Submitted', { cartItems, deliveryDetails, paymentDetails });
    // Process the order
  };

  return (
    <main className="checkout-container">
      <h1>Checkout</h1>

      {/* Cart Items Section */}
      <section className="cart-items">
        <h2>Your Cart</h2>

        {/* Header Row */}
        <div className="cart-header">
          <p>Item Name</p>
          <p>Weight</p>
          <p>Quantity</p>
          <p>Price</p>
        </div>

        {/* Cart Items */}
        {cartItems.map((item) => (
          <div key={item.id} className="cart-item">
            <p>{item.brand + " " + item.name}</p>
            <p>{(item.weight * item.quantity).toFixed(2)} lbs</p>
            <p>{item.quantity}</p>
            <p>${(item.price*item.quantity).toFixed(2)}</p>
          </div>
        ))}

        {/* Total Price */}
        
        <div className="total-price">
          {
            Number(totalWeight) > 20 ? (
              <>
                 <p>Shipping Free: $5.00</p>
                 <h3>Total: ${Number(totalPrice + 5).toFixed(2)}</h3>
              </>
             
            ) : <h3>Total: ${Number(totalPrice).toFixed(2)}</h3>
          }
          
        </div>
      </section>

      {/* Delivery Information Form */}
      <section className="delivery-info">
        <h2>Delivery Information</h2>
        <form>
          <label>
            Address:
            <input type="text" name="address" value={deliveryDetails.address} onChange={(e) => handleInputChange(e, "delivery")} required />
          </label>
          <label>
            City:
            <input type="text" name="city" value={deliveryDetails.city} onChange={(e) => handleInputChange(e, "delivery")} required />
          </label>
          <label>
            ZIP Code:
            <input type="text" name="zip" value={deliveryDetails.zip} onChange={(e) => handleInputChange(e, "delivery")} required />
          </label>
        </form>
      </section>

      {/* Payment Information Form */}
      <section className="payment-info">
        <h2>Payment Information</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Name on Card:
            <input type="text" name="cardName" value={paymentDetails.cardName} onChange={(e) => handleInputChange(e, "payment")} required />
          </label>
          <label>
            Card Number:
            <input type="text" name="cardNumber" value={paymentDetails.cardNumber} onChange={(e) => handleInputChange(e, "payment")} required />
          </label>
          <label>
            Expiry Date:
            <input type="text" name="expiryDate" value={paymentDetails.expiryDate} onChange={(e) => handleInputChange(e, "payment")} required />
          </label>
          <label>
            CVV:
            <input type="text" name="cvv" value={paymentDetails.cvv} onChange={(e) => handleInputChange(e, "payment")} required />
          </label>
          <button type="submit">Place Order</button>
        </form>
      </section>
    </main>
  );
}

export default CheckoutPage;