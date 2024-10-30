import { useState, useEffect } from 'react'
import axios from 'axios';
import LandingPage from './components/LandingPage/LandingPage'
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link
} from "react-router-dom";
import ProductPage from './components/ProductPage/ProductPage';
import CheckoutPage from './components/CheckoutPage/CheckoutPage';
import MainLayout from './components/MainLayout';
import { SearchPage } from './components/SearchPage/SearchPage';


function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route path ="/" element = {<LandingPage />} />
            <Route path ="/product" element = {<ProductPage />} />
            <Route path ="/checkout" element = {<CheckoutPage />} />
            <Route path ="/search" element = {<SearchPage />} />
            {/* <Route path ="/search?q=*" element = {<SearchPage />} /> */}
          </Route>
        </Routes>
      </Router>
    </>
  )
}

export default App
