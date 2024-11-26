import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import LandingPage from './components/LandingPage/LandingPage.jsx'
import ProductPage from './components/ProductPage/ProductPage.jsx'
import CheckoutPage from './components/CheckoutPage/CheckoutPage.jsx'

import {
  createBrowserRouter,
  RouterProvider,
} from 'react-router-dom';

// const router = createBrowserRouter([
//   {
//     path: "/",
//     element: <LandingPage />
//   },
//   {
//     path: "/product",
//     element: <ProductPage />
//   },
//   {
//     path: "/checkout",
//     element: <CheckoutPage />
//   }
// ])


createRoot(document.getElementById('root')).render(
  <StrictMode>
    {/* <RouterProvider router={router} /> */}
    <App />
  </StrictMode>,
)
