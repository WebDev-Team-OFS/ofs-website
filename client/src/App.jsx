import { useState, useEffect } from 'react'
import axios from 'axios';
import LandingPage from './components/LandingPage/LandingPage'
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";
import ProductPage from './components/ProductPage/ProductPage';
import CheckoutPage from './components/CheckoutPage/CheckoutPage';
import MainLayout from './components/MainLayout';
import { SearchPage } from './components/SearchPage/SearchPage';
import AdminLogin from './components/AdminLogin/AdminLogin';
import LoginPage from './components/LoginPage/LoginPage';
import ShoppingCartPage from './components/ShoppingCartPage/ShoppingCartPage';
import ProfilePage from './components/ProfilePage/ProfilePage';
import AdminProducts from './components/AdminProducts/AdminProducts';
import AdminAccounts from './components/AdminAccounts/AdminAccounts';


function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/login" element= {<LoginPage />} />
          <Route path="/admin/login" element= {<AdminLogin />} />
          <Route path="/admin/products" element= {<AdminProducts />} />
          <Route path="/admin/accounts" element= {<AdminAccounts />} />
          <Route path="/" element={<MainLayout />}>
            <Route path ="/" element = {<LandingPage />} />
            <Route path ="/product/:id" element = {<ProductPage />} />
            <Route path ="/checkout" element = {<CheckoutPage />} />
            <Route path ="/cart" element = {<ShoppingCartPage />} />
            <Route path ="/search" element = {<SearchPage />} />
            <Route path ="/profile" element = {<ProfilePage />} />
            {/* <Route path ="/search?q=*" element = {<SearchPage />} /> */}
          </Route>
        </Routes>
      </Router>
    </>
  )
}

export default App
