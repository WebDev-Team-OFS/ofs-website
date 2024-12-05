import { useEffect, useState } from "react";
import GroceryCard from "../GroceryCard/GroceryCard"
import axios from "axios";


function FeaturedItems() {
    const [featuredItems, updateFeaturedItems] = useState([])

    const fetchData = async () => {
        let response = await axios.get(`http://127.0.0.1:8080/api/search?q=`)
        
        updateFeaturedItems(response.data.products.filter(grocery => grocery.featured === 1));
    }

    const customScroll = () => {
        const featuredItems = document.querySelector(".featured-items");
        const leftArrow = document.querySelector(".leftArrow");
        const rightArrow = document.querySelector(".rightArrow");



        featuredItems.addEventListener("wheel", (e) => {
            e.preventDefault();
            featuredItems.scrollLeft += e.deltaX;
            featuredItems.scrollLeft += e.deltaY;
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
                                key = {grocery.product_id}
                                product ={grocery}
                            />   
                        ))
                    ) : (
                        <p>No groceries found.</p> 
                    )}
                </div>
                <button className="rightArrow arrow">&#62;</button>
            </div>
        </div>
    </>
   )
}

export default FeaturedItems;