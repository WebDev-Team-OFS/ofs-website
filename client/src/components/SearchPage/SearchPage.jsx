import React, { useState, useEffect } from 'react'
import GroceryCard from '../GroceryCard/GroceryCard'
import './search-page.css'
import { useLocation } from 'react-router-dom'
import axios from 'axios'
import { useNavigate } from 'react-router-dom';


export const SearchPage = () => {
    const navigate = useNavigate();

    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const query = queryParams.get('q');
    const categoryQuery = queryParams.get('category');
    console.log(query);
    console.log(categoryQuery);
    const categories = ["Meats", "Produce", "Canned Foods", "Frozen Foods", "Snacks", "Drinks", "Grains", "Ingredients", "Baked", "Dairy"]

    const [groceries, setGroceries] = useState([]);
    const [categoryIndex, setCategoryIndex] = useState(-1);

    const fetchData = async () => {
        console.log("fetch data");
        let response;
        if (categoryQuery == null) {
            response = await axios.get(`http://127.0.0.1:8080/api/search?q=${query}`);
        }
        else {
            response = await axios.get(`http://127.0.0.1:8080/api/search?q=${query}&category=${categoryQuery}`);
        }
        
        console.log(response.data.products);
        //console.log("fetch data");
        setGroceries(response.data.products);
    }

    const selectCategory = (index) => {
        if (categoryIndex === index) {
            setCategoryIndex(-1);
            index = -1;
            navigate(`/search?q=${query}`);
        }
        else {
            setCategoryIndex(index);    
            navigate(`/search?q=${query}&category=${categories[index]}`);
        }
       
    }

    
    
    useEffect(() => {
        fetchData();
    }, [query, categoryIndex])

  return (
    <div className="search-page-container">
        <aside className="categories-sidebar">
            <h3>Categories</h3>
            {categories.map((category, index) => {
                return <button key={category} onClick={() =>selectCategory(index)} className={(categoryIndex === index ? 'active' : '') + (index === categories.length-1 ? ' end' : '')}>
                    {category}
                </button>
            })}
        </aside>
           <div className="search-products-container">
                {groceries.length > 0 ? (
                    groceries.map(grocery => (
                        <GroceryCard 
                            product ={grocery}
                        />
                    ))
                ) : (
                    <p>No groceries found.</p> 
                )}
            </div>
    </div>
    
  )
}
