import './product-page.css'
import { useLocation, useParams } from 'react-router-dom'
import {useEffect, useState} from 'react'
import axios from 'axios'




function ProductPage() {

    const [product, setProduct] = useState({});

    const param = useParams();
    const id = param.id;

    const fetchData = async () => {
        console.log("fetch data");
        let response = await axios.get(`http://127.0.0.1:8080/api/product/${id}`); 
        console.log(response.data.product);
        setProduct(response.data.product);
    }

    useEffect(() => {
        fetchData();
    }, [])
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