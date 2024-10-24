import { useEffect } from "react";


function Categories() {
    const customScroll = () => {
        console.log("hello");
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
    })


   return (
    <>
        <div className="categories-container">
            <h1>Search by Category</h1>
           
                <div className="categories">
                    <div className="image-container">
                        <img src="./src/img/categories/meats-category.jpg" alt="" />
                        <p>Meat</p>
                    </div>
                    <div className="image-container">
                        <img src="./src/img/categories/vegetables-category.jpg" alt="" />
                        <p>Vegetables</p>
                    </div>
                    <div className="image-container">
                        <img src="./src/img/categories/drinks-category.jpg" alt="" />
                        <p>Drinks</p>
                    </div>
                    <div className="image-container">
                        <img src="./src/img/categories/canned-foods-category.jpg" alt="" />
                        <p>Canned Foods</p>
                    </div>
                    <div className="image-container">
                        <img src="./src/img/categories/snacks-category.jpg" alt="" />
                        <p>Snacks</p>
                    </div>
                </div>
                
        </div>
    </>
   )
}

export default Categories;