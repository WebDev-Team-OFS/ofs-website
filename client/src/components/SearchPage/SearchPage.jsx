import React, { useState, useEffect } from 'react'
import GroceryCard from '../GroceryCard/GroceryCard'
import './search-page.css'
import { useLocation } from 'react-router-dom'
import axios from 'axios'

export const SearchPage = () => {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const query = queryParams.get('q');
    console.log(query);

    const [groceries, setGroceries] = useState([]);

    const fetchData = async () => {
        console.log("fetch data");
        const response = await axios.get(`http://127.0.0.1:8080/api/search?query=${query}`);
        console.log(response.data.products);
        console.log("fetch data");
        setGroceries(response.data.products);
    }
    
    useEffect(() => {
        fetchData();
    }, [query])

  return (
    <div className="search-page-container">
        <aside className="categories-sidebar">
            <h3>Categories</h3>
            <p>Meats</p>
            <p>Fruits</p>
            <p>Vegetables</p>
            <p>Canned Foods</p>
            <p>Frozen Foods</p>
            <p>Snacks</p>
            <p>Drinks</p>
            <p>Grains</p>
            <p>Ingredients</p>
            <p className="end">Pet Foods</p>

        </aside>
        {/* <div className="search-products-container">
            <GroceryCard price="8.99" title="Kirkland Large Farm Eggs, 12 count" weight="1.25" imageURL="/src/img/food/eggs.png" />
            <GroceryCard price = "13.99" title="Loaf of Nature's Whole Weat Bread" weight="1.25" imageURL="/src/img/food/bread.jpg" />
            <GroceryCard price = "11.99" title = "Daidy Free Plain Yogurt" weight="2.00" imageURL="/src/img/food/yogurt.png" />
            <GroceryCard price ="5.99" title="Lunchly Fiesta Nachoes With Prime" weight="2.50" imageURL="/src/img/food/lunchly.png" />
            <GroceryCard price ="2.99" title ="Signature Select Baby-Cut Carrots" weight="0.50" imageURL="/src/img/food/baby-carrots.png" />
            <GroceryCard price ="7.99" title="Pavesi Gocciole Chocolate Chip Cookies" weight="1.00" imageURL="/src/img/food/cookies.png" />
            <GroceryCard price="8.99" title="Kirkland Large Farm Eggs, 12 count" weight="1.25" imageURL="/src/img/food/eggs.png" />
            <GroceryCard price = "13.99" title="Loaf of Nature's Whole Weat Bread" weight="1.25" imageURL="/src/img/food/bread.jpg" />
            <GroceryCard price = "11.99" title = "Daidy Free Plain Yogurt" weight="2.00" imageURL="/src/img/food/yogurt.png" />
            <GroceryCard price ="5.99" title="Lunchly Fiesta Nachoes With Prime" weight="2.50" imageURL="/src/img/food/lunchly.png" /> 
            <GroceryCard price ="2.99" title ="Signature Select Baby-Cut Carrots" weight="0.50" imageURL="/src/img/food/baby-carrots.png" />
            <GroceryCard price ="7.99" title="Pavesi Gocciole Chocolate Chip Cookies" weight="1.00" imageURL="/src/img/food/cookies.png" />
        </div> */}
           <div className="search-products-container">
                {groceries.length > 0 ? (
                    groceries.map(grocery => (
                        <GroceryCard 
                            key={grocery.id} 
                            price={grocery.price} 
                            title={grocery.brand + " " + grocery.name} 
                            weight={grocery.weight} 
                            imageURL={grocery.imageURL} // Assuming your API returns this
                        />
                    ))
                ) : (
                    <p>No groceries found.</p> // Handle the case where no groceries are returned
                )}
            </div>
    </div>
    
  )
}
