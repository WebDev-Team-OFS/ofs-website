import React from 'react'
import GroceryCard from '../GroceryCard/GroceryCard'
import './search-page.css'

export const SearchPage = () => {
  return (
    <div class="search-page-container">
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
        <div className="search-products-container">
            <GroceryCard price="8.99" title="Kirkland Large Farm Eggs, 12 count" weight="1.25" imageURL="./src/img/food/eggs.png" />
            <GroceryCard price = "13.99" title="Loaf of Nature's Whole Weat Bread" weight="1.25" imageURL="./src/img/food/bread.jpg" />
            <GroceryCard price = "11.99" title = "Daidy Free Plain Yogurt" weight="2.00" imageURL="./src/img/food/yogurt.png" />
            <GroceryCard price ="5.99" title="Lunchly Fiesta Nachoes With Prime" weight="2.50" imageURL="./src/img/food/lunchly.png" />
            <GroceryCard price ="2.99" title ="Signature Select Baby-Cut Carrots" weight="0.50" imageURL="./src/img/food/baby-carrots.png" />
            <GroceryCard price ="7.99" title="Pavesi Gocciole Chocolate Chip Cookies" weight="1.00" imageURL="./src/img/food/cookies.png" />
            <GroceryCard price="8.99" title="Kirkland Large Farm Eggs, 12 count" weight="1.25" imageURL="./src/img/food/eggs.png" />
            <GroceryCard price = "13.99" title="Loaf of Nature's Whole Weat Bread" weight="1.25" imageURL="./src/img/food/bread.jpg" />
            <GroceryCard price = "11.99" title = "Daidy Free Plain Yogurt" weight="2.00" imageURL="./src/img/food/yogurt.png" />
            <GroceryCard price ="5.99" title="Lunchly Fiesta Nachoes With Prime" weight="2.50" imageURL="./src/img/food/lunchly.png" /> 
            <GroceryCard price ="2.99" title ="Signature Select Baby-Cut Carrots" weight="0.50" imageURL="./src/img/food/baby-carrots.png" />
            <GroceryCard price ="7.99" title="Pavesi Gocciole Chocolate Chip Cookies" weight="1.00" imageURL="./src/img/food/cookies.png" />
        </div>
    </div>
    
  )
}
