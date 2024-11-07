import { formToJSON } from 'axios'
import './product-page.css'
import { useLocation } from 'react-router-dom'



function ProductPage() {
    const location = useLocation();
    const {product} = location.state || {};
    return (
        <>
            <div className="product-page-container">
                <div className="product-image-container">
                    <img src={product.imageURL} alt="" />
                </div>
                <div className="product-content">
                    <h1 className="product-title">{product.brand + " " + product.name}</h1>
                    <div className="price-weight">
                        <p className="product-price">${product.price}</p>
                        <p className="product-weight">{product.weight} lbs</p>
                    </div>
                    <p className="product-description">
                        {product.description}
                    </p>
                    <button>ADD TO CART</button>
                </div>
            </div>
        </>
    )
}

{/* <GroceryCard price ="7.99" title="Pavesi Gocciole Chocolate Chip Cookies" weight="1.00" imageURL="./src/img/food/cookies.png" /> */}


export default ProductPage