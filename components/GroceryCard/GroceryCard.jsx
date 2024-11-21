import './grocery-card.css'
import { useNavigate } from 'react-router-dom';


function GroceryCard({product}) {
    const navigate = useNavigate();

    const goToProduct = () => {
        console.log("hello");
        console.log(product);

     navigate(`/product/${product.product_id}`);

    }

    return(
        <>
            <div className="grocery-card" onClick={goToProduct}>
                <img src={product.imageURL} alt="" />
                <div>
                    <p className="price">${product.price}</p>
                    <p className="title">{product.brand + " " + product.name}</p>
                    <p className="weight">{product.weight} lbs</p>
                </div>
                <button>ADD TO CART</button>
            </div>
        </>
    )
}

export default GroceryCard