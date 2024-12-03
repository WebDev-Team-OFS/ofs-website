import React, {useEffect, useState} from "react"
import './product-form.css'

function ProductForm({product, onCancel}) {
    const [productInfo, setProductInfo] = useState({
        brand: product.brand,
        name: product.name,
        category: product.category,
        price: product.price,
        weight: product.weight,
        stock: product.stock,
        featured: product.featured,
        description: product.description,
    })

    const test = () => {
        console.log(product.brand);
        console.log(product.name);
        console.log(product.featured);
    }

    const updateForm = (e) => {
        const { name, type, checked, value } = e.target;
  
        // If it's a checkbox, use 'checked' to set the value
        const newValue = type === 'checkbox' ? checked : value;
      
        setProductInfo((prev) => ({
          ...prev,
          [name]: newValue,
        }));
        console.log(productInfo.featured)
    }

    const handleCancel = (e) => {
        e.preventDefault();
        onCancel();
    }

    useEffect(() => {
        test();
    }, [])

    return(
        <>
            <form className="product-form" action="" >
                <div className="product-form-image-wrapper">
                    <img src={`http://127.0.0.1:8080/api/image/${product.product_id}`} alt="" />
                </div>
            <div className="input-wrapper">
                <label htmlFor="brand">Brand</label>
                <input type="text" id="brand" name="brand" value={productInfo.brand} onChange={updateForm} />
            </div>
            <div className="input-wrapper">
                <label htmlFor="name">Name</label>
                <input type="text" id="name" name="name" value={productInfo.name} onChange={updateForm} />
            </div>
            <div className="input-wrapper">
                <label htmlFor="price">Price ($)</label>
                <input type="text" id="price" name="price" value={productInfo.price} onChange={updateForm} />
            </div>
            <div className="input-wrapper">
                <label htmlFor="weight">Weight (lbs)</label>
                <input type="text" id="weight" name="weight" value={productInfo.weight} onChange={updateForm} />
            </div>
            <div className="input-wrapper">
                <label htmlFor="stock">Stock</label>
                <input type="text" id="stock" name="stock" value={productInfo.stock} onChange={updateForm} />
            </div>
            <div className="input-wrapper">
                <label htmlFor="description">Description</label>
                <textarea id="description" name="description" rows="6" value={productInfo.description} onChange={updateForm} />
            </div>
            <div className="input-wrapper-featured">
                <label htmlFor="description">Featured</label>
                <input type="checkbox" id="featured" name="featured" value={productInfo.featured} checked={productInfo.featured} onChange={updateForm} />
            </div>
            <div className="buttons">
                <button className="submit-changes">Submit Changes</button>
                <button className="cancel-product-form" onClick={handleCancel}>Cancel</button>
            </div>
          
        </form>
        </>
    )
}

export default ProductForm;