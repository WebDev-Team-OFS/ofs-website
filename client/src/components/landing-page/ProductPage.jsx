import NavigationBar from "./NavigationBar"
import './landing-page.css'
import './product-page.css'



function ProductPage({imageURL, price, title, weight, description}) {
    return (
        <main>
            <NavigationBar />
            <div className="product-page-container">
                <div className="product-image-container">
                    <img src="./src/img/food/cookies.png" alt="" />
                </div>
                <div className="product-content">
                    <h1 className="product-title">Pavesi Gocciole Chocolate Chip Cookies</h1>
                    <div className="price-weight">
                        <p className="product-price">$7.99</p>
                        <p className="product-weight">1.00 lbs</p>
                    </div>
                    <p className="product-description">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer semper dictum massa et elementum.
                    Proin laoreet mi non turpis molestie ultricies. Vestibulum malesuada pellentesque urna vel vulputate. 
                    Nulla sodales vel nulla vel convallis. Vestibulum ac urna porttitor, condimentum sapien ut, auctor lacus. 
                    </p>
                    <button>ADD TO CART</button>
                </div>
            </div>
        </main>
    )
}

{/* <GroceryCard price ="7.99" title="Pavesi Gocciole Chocolate Chip Cookies" weight="1.00" imageURL="./src/img/food/cookies.png" /> */}


export default ProductPage