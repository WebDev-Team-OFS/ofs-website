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
        { categoryName: "Meat", imageName: "meats-category.jpg" },
        { categoryName: "Produce", imageName: "produce-category.jpg" },
        { categoryName: "Canned Foods", imageName: "canned-foods-category.jpg" },
        { categoryName: "Frozen Foods", imageName: "meats-category.jpg" }, //TODO
        { categoryName: "Snacks", imageName: "snacks-category.jpg" },
        { categoryName: "Drinks", imageName: "drinks-category.jpg" },
        { categoryName: "Grains", imageName: "meats-category.jpg" }, //TODO
        { categoryName: "Ingredients", imageName: "meats-category.jpg" }, //TODO
        { categoryName: "Baked", imageName: "meats-category.jpg" }, //TODO
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
                        <div className="image-container">
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