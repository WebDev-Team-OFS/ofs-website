import './grocery-card.css'

function GroceryCard({imageURL, price, title, weight}) {
    return(
        <>
            <div className="grocery-card">
                <img src={imageURL} alt="" />
                <div>
                    <p className="price">${price}</p>
                    <p className="title">{title}</p>
                    <p className="weight">{weight} lbs</p>
                </div>
                <button>ADD TO CART</button>
            </div>
        </>
    )
}

export default GroceryCard