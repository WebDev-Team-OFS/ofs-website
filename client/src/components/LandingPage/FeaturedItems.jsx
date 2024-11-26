import { useEffect, useState } from "react";
import GroceryCard from "../GroceryCard/GroceryCard"
import axios from "axios";


function FeaturedItems() {
    const [featuredItems, updateFeaturedItems] = useState([])

    const fetchData = async () => {
        let response = await axios.get(`http://127.0.0.1:8080/api/search?q=`)
        console.log("FeaturedItems");
        console.log(response.data.products)
        
        updateFeaturedItems(response.data.products.filter(grocery => grocery.featured === 1));
    }

    const customScroll = () => {
        const featuredItems = document.querySelector(".featured-items");
        const leftArrow = document.querySelector(".leftArrow");
        const rightArrow = document.querySelector(".rightArrow");



        featuredItems.addEventListener("wheel", (e) => {
            e.preventDefault();
            featuredItems.scrollLeft += e.deltaX;
            featuredItems.style.scrollBehavior = "auto";

        });

        leftArrow.addEventListener("click", () => {
            featuredItems.style.scrollBehavior = "smooth";

            featuredItems.scrollLeft -= 270;
        })

        rightArrow.addEventListener("click", () => {
            featuredItems.style.scrollBehavior = "smooth";
            featuredItems.scrollLeft += 270;
        })
    }

    useEffect(() => {
        customScroll();
        fetchData();
    }, [])


   return (
    <>
        <div className="featured-items-container">
            <h1>Featured Items</h1>
            <div className="featured-items-with-arrows">
                <button className="leftArrow arrow">&#60;</button>
                <div className="featured-items">
                    {featuredItems.length > 0 ? (
                        featuredItems.map(grocery => (
                            <GroceryCard 
                                product ={grocery}
                            />   
                        ))
                    ) : (
                        <p>No groceries found.</p> 
                    )}
                    {/* <GroceryCard price="8.99" title="Kirkland Large Farm Eggs, 12 count" weight="1.25" imageURL="./src/img/food/eggs.png" />
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
                    <GroceryCard price ="7.99" title="Pavesi Gocciole Chocolate Chip Cookies" weight="1.00" imageURL="./src/img/food/cookies.png" /> */}
                </div>
                <button className="rightArrow arrow">&#62;</button>
            </div>
        </div>
    </>
   )
}

export default FeaturedItems;