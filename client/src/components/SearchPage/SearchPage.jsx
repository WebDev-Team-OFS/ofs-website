import { useState, useEffect } from 'react'
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
    const filterQuery = queryParams.get('filter');
    
    const categories = ["Meats", "Produce", "Canned Foods", "Frozen Foods", "Snacks", "Drinks", "Grains", "Ingredients", "Baked", "Dairy"]

    const [groceries, setGroceries] = useState([]);
    const [categoryIndex, setCategoryIndex] = useState(-1);
    const [filter, setFilter] = useState("");

    const fetchData = async () => {
        console.log("fetch data");
        let response = await axios.get(`http://127.0.0.1:8080/api/search?q=${query}`);
        let products = response.data.products;
        console.log(categoryQuery);
        if (categoryQuery) {
            products = products.filter(product => product.category === categoryQuery);
            setCategoryIndex(categories.indexOf(categoryQuery));
        }
        if (filterQuery) {
            if (filterQuery === "price-low-to-high") {
                products = products.sort((productOne, productTwo) => productOne.price - productTwo.price);
                setFilter(filterQuery);
            }
            else if (filterQuery === "price-high-to-low") {
                products = products.sort((productOne, productTwo) => productTwo.price - productOne.price)
                setFilter(filterQuery);
            }
            else if (filterQuery === "a-to-z") {
                products = products.sort((productOne, productTwo) => productOne.brand.toLowerCase().localeCompare(productTwo.brand.toLowerCase()));
                setFilter(filterQuery);
            }
            else if (filterQuery === "z-to-a") {
                products = products.sort((productOne, productTwo) => productTwo.brand.toLowerCase().localeCompare(productOne.brand.toLowerCase()));
                setFilter(filterQuery);
            }
        }
        console.log(response.data.products);
        setGroceries(products);
    }

    const selectCategory = (index) => {
        if (categoryIndex === index) {
            setCategoryIndex(-1);
            index = -1;
            if (filterQuery) {
                navigate(`/search?q=${query}&filter=${filterQuery}`);
            }
            else {
                navigate(`/search?q=${query}`);
            }
            
        }
        else {
            setCategoryIndex(index);    
            if (filterQuery) {
                navigate(`/search?q=${query}&category=${categories[index]}&filter=${filterQuery}`);
            }
            else{
                navigate(`/search?q=${query}&category=${categories[index]}`);
            }
        }
       
    }

    const selectFilter = (event) => {
        setFilter(event.target.value);
        console.log(event.target.value);
        if (categoryQuery) {
            navigate(`/search?q=${query}&category=${categoryQuery}&filter=${event.target.value}`);
        }
        else {
            navigate(`/search?q=${query}&filter=${event.target.value}`);
        }
    };
    
    useEffect(() => {
        fetchData();
    }, [query, categoryIndex, filter])

  return (
    <div className="search-page-container">
        <aside className="sidebar">
            <div className="categories-sidebar">
                <h3>Categories</h3>
                {categories.map((category, index) => {
                    return <button key={category} onClick={() =>selectCategory(index)} className={(categoryIndex === index ? 'active' : '') + (index === categories.length-1 ? ' end' : '')}>
                        {category}
                    </button>
                })}
            </div>
            <select className="filters" value={filter} onChange={selectFilter}>
                <option value="">Filter by</option>
                <option value="price-low-to-high">Price: Low to High</option>
                <option value="price-high-to-low">Price: High to Low</option>
                <option value="a-to-z">Alphabetically: A to Z</option>
                <option value="z-to-a">Alphabetically: Z to A</option>
            </select>
        </aside>
           <div className="search-products-container">
                {groceries.length > 0 ? (
                    groceries.map(grocery => (
                        <GroceryCard 
                            key = {grocery.id}
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
