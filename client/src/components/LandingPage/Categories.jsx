import { useEffect } from "react";
import './categories.css';
import { useNavigate } from 'react-router-dom';



function Categories() {
    const navigate = useNavigate();

    const searchCategory = (categoryName) => {
        console.log("hello");
        navigate(`/search?q=&category=${categoryName}`);
    }

    const customScroll = () => {
        const featuredItems = document.querySelector(".categories");
        const leftArrow = document.querySelector(".category-leftArrow");
        const rightArrow = document.querySelector(".category-rightArrow");
        console.log("hello");


        featuredItems.addEventListener("wheel", (e) => {
            e.preventDefault();
            featuredItems.scrollLeft += e.deltaX;
            featuredItems.scrollLeft += e.deltaY;
            featuredItems.style.scrollBehavior = "auto";


        });

        leftArrow.addEventListener("click", () => {
            featuredItems.style.scrollBehavior = "smooth";

            featuredItems.scrollLeft -= 270;
            console.log("arr0w");
        })

        rightArrow.addEventListener("click", () => {
            featuredItems.style.scrollBehavior = "smooth";
            featuredItems.scrollLeft += 270;
        })
    }

    const categoriesList = [
        { categoryName: "Meats", imageName: "meats-category.jpg", key: "0" },
        { categoryName: "Produce", imageName: "produce-category.jpg", key: "1"},
        { categoryName: "Canned Foods", imageName: "canned-foods-category.jpg", key: "2"},
        { categoryName: "Snacks", imageName: "snacks-category.jpg", key: "4" },
        { categoryName: "Drinks", imageName: "drinks-category.jpg", key: "5" },
        { categoryName: "Grains", imageName: "grains-category.jpg", key: "6"}, 
        { categoryName: "Ingredients", imageName: "ingredients-category.jpg", key: "7" }, 
        { categoryName: "Dairy", imageName: "dairy-category.jpg", key: "9"}, 
    ]

    useEffect(() => {
        customScroll();
    })


   return (
    <>
        <div className="categories-container">
            <h1>Search by Category</h1>
            <div className="categories-with-arrows">
                 
                    
                <button className="category-leftArrow arrow">&#60;</button>
                    <div className="categories">
                    {
                    categoriesList.map(category => (
                        <div key = {category.key} className="image-container">
                            <img src={`./src/img/categories/${category.imageName}`}alt="" onClick={() => searchCategory(category.categoryName)} />
                            <p>{category.categoryName}</p>
                        </div>
                    ))
                   }
                    </div>
                <button className="category-rightArrow arrow">&#62;</button>
            </div>  
        </div>
    </>
   )
}

export default Categories;