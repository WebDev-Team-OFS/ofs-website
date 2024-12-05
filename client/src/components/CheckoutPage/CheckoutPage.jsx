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

  const [error, setError] = useState("");
  const [showError, setShowError] = useState(false);

  const [isSuccess, setIsSuccess] = useState(false);

  

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
      navigate('/')
    }
    for (let i = 0; i < tempCart.length; i++) {
        console.log(tempCart[i].product_id)
        try{
            let response = await axios.get(`http://127.0.0.1:8080/api/product/${tempCart[i].product_id}`);
                
            response.data.product.quantity = tempCart[i].quantity;
            cart.push(response.data.product);
        }
        catch (error) {
            console.log(error);
        }        
    }
    setCartItems(cart);
  }

  

  useEffect(() => {
    getCart();
  }, [])

  const [deliveryDetails, setDeliveryDetails] = useState({
    address: '',
    city: '',
    state: '',
    zip: ''
  });

  const validateInputs = () => {
    const validZip = /^\d{5}(-\d{4})?$/;
    const validCVV = /^\d{3,4}$/;
    const validStates = [
      'alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware', 
      'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 
      'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 
      'missouri', 'montana', 'nebraska', 'nevada', 'new hampshire', 'new jersey', 'new mexico', 
      'new york', 'north carolina', 'north dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 
      'rhode island', 'south carolina', 'south dakota', 'tennessee', 'texas', 'utah', 'vermont', 
      'virginia', 'washington', 'west virginia', 'wisconsin', 'wyoming'
    ];

  

    if (deliveryDetails.address == "" || deliveryDetails.city == "" || deliveryDetails.zip == "" ) {
      setError("Enter all your delivery information");
      setShowError(true)
      return false;
    }
    console.log(deliveryDetails.state.toLowerCase());
    if (!validStates.includes(deliveryDetails.state.toLowerCase())) {
      setError("Please enter a valid state");
      setShowError(true)
      return false;
    }
    if (!validZip.test(deliveryDetails.zip)) {
      setError("Please enter a valid zip code");
      setShowError(true)
      return false;
    }
    if (!validCVV.test(paymentDetails.cvv)) {
      setError("Please enter a valid CVV");
      setShowError(true)
      return false;
    }
    setError("");
    setShowError(false)
    return true;
  }

  const [paymentDetails, setPaymentDetails] = useState({
    card_name: '',
    card_number: '',
    expiry_date: '',
    cvv: ''
  });

  const [expiryDate, setExpiryDate] = useState('');

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

  const handleExpiryInputChange = (e) => {
    let input = e.target.value;

    input = input.replace(/\D/g, '');
    
    if (input.length > 2) {
      input = input.substring(0, 2) + '/' + input.substring(2, 4);
    }

    if (input.length > 5) {
      input = input.substring(0, 5);
    }
    setExpiryDate(input);
  }

  // Form submission handler
  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setShowError(false)
    console.log(deliveryDetails);
    console.log(paymentDetails);
    if (!validateInputs()) {
      return;
    }

    if (await checkLoginHelper()) {
      //check if credit card number is valid
      try {
        const response = await axios.post('http://127.0.0.1:8080/api/validate-card', paymentDetails, {
          headers: {
              'Content-Type': 'application/json', 
          }  
      });
      }
      catch (e) {
        if (e.response?.data?.error) {
          setError(e.response.data?.error);
          setShowError(true)
        }
        else {
          setError("There was an error while checking out");
          setShowError(true)
        }
        return;
      }

      //check if expiration date is valid
      try {
        const response = await axios.post('http://127.0.0.1:8080/api/validate-expiration', {"expiry_date":expiryDate}, {
          headers: {
              'Content-Type': 'application/json', 
          }  
      });
      }
      catch (e) {
        if (e.response?.data?.error) {
          setError(e.response.data?.error);
          setShowError(true)
        }
        else {
          setError("Expiration date is invalid");
          setShowError(true)
        }
        return;
      }
      console.log("CREDIT CARD HAS BEEN VALIDATED")
      try {
          const response = await axios.post('http://127.0.0.1:8080/api/checkout', {}, {
              headers: {
                  "Authorization": `Bearer ${localStorage.getItem("access_token")}`
              }  
          });
          console.log("CHECKOUT CART");
      }
      catch (e) {
        console.log("CHECKOUT ERROR")
        console.log(e.response.data.error)
        if (e.response?.data?.error) {
          setError(e.response.data.error);
        }
        else {
          setError("There was an error while checking out")
        }
        setShowError(true)
        return;
      }
      setError("");
      setShowError(false)
      setIsSuccess(true);
      setTimeout(() => {
        navigate('/');  
      }, 2500);
   }
   else {
      setError("You are not logged in");
      setShowError(true)
   }
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
          <div key={item.product_id} className="cart-item">
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
        <form onSubmit={handleSubmit}>
          <label>
            Address:
            <input type="text" name="address" value={deliveryDetails.address} onChange={(e) => handleInputChange(e, "delivery")} required />
          </label>
          <label>
            City:
            <input type="text" name="city" value={deliveryDetails.city} onChange={(e) => handleInputChange(e, "delivery")} required />
          </label>
          <label>
            State:
            <input type="text" name="state" value={deliveryDetails.state} onChange={(e) => handleInputChange(e, "delivery")} required />
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
            <input type="text" name="card_name" value={paymentDetails.card_name} onChange={(e) => handleInputChange(e, "payment")} required />
          </label>
          <label>
            Card Number:
            <input type="text" name="card_number" value={paymentDetails.card_number} onChange={(e) => handleInputChange(e, "payment")} required />
          </label>
          <label>
            Expiry Date:
            <input type="text" name="expiry_date" value={expiryDate} onChange={handleExpiryInputChange} required  placeholder="MM/YY"/>
          </label>
          <label>
            CVV:
            <input type="text" name="cvv" value={paymentDetails.cvv} onChange={(e) => handleInputChange(e, "payment")} required />
          </label>
          <button type="submit">Place Order</button>
        </form>
        {showError && <div className="product-form-error-message">{error}</div>}
        {isSuccess && <div className="checkout-success">Thank you for shopping with OFS!</div>}
      </section>
    </main>
  );
}

export default CheckoutPage;