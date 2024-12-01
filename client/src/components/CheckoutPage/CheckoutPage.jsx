import NavigationBar from '../NavigationBar/NavigationBar';
import React, { useState, useEffect } from 'react';
import './checkout-page.css'; // Link to your CSS file for styling
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { checkLoginHelper } from '../utils';

function CheckoutPage() {
  const navigate = useNavigate();

  const [cartItems, setCartItems] = useState([])

  const [isLoggedIn, setIsLoggedIn] = useState(false);

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
    else {
        tempCart = JSON.parse(localStorage.getItem("cart")) || [];
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
  let totalPrice = cartItems.reduce((total, item) => total + item.price * item.quantity, 0);
  let totalWeight = cartItems.reduce((total, item) => total + item.weight * item.quantity, 0);

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
  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log(localStorage.getItem("access_token"));
    if (await checkLoginHelper()) {
      try {
          const response = await axios.post('http://127.0.0.1:8080/api/checkout', {}, {
              headers: {
                  "Authorization": `Bearer ${localStorage.getItem("access_token")}`
              }  
          });
          console.log("CHECKOUT CART");
          navigate(`/`)
      }
      catch {
          console.log("DID NOT CHECKOUT CART")
      }
   }
   else {
    totalPrice = cartItems.reduce((total, item) => total + item.price * item.quantity, 0);
    totalWeight = cartItems.reduce((total, item) => total + item.weight * item.quantity, 0);

    const cart = JSON.parse(localStorage.getItem("cart")) || []
    const order = {
      items: cart,
      total_price: Number(totalPrice),
      total_weight: Number(totalWeight),
    }
    console.log(order);
    try {
      const response = await axios.post('http://127.0.0.1:8080/api/guest_checkout', {order});

      console.log('Order Submitted', { cartItems, deliveryDetails, paymentDetails });
      localStorage.removeItem('cart');
      navigate('/');
      alert("Your order has been submitted!")
    }
    catch (error) {
      console.log("Cart not sent successfully: ", error);
    }
   }

    
    
    
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