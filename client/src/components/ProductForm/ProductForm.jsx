import React, {useEffect, useState} from "react"
import './product-form.css'
import axios from 'axios'
import { checkAdminLoginHelper } from "../utils"
import { useNavigate } from "react-router-dom"

function ProductForm({product, onCancel}) {

    const [productInfo, setProductInfo] = useState(() => {
        if(product) {
            return {
                brand: product.brand,
                name: product.name,
                category: product.category,
                price: product.price,
                weight: product.weight,
                stock: product.stock,
                featured: product.featured,
                description: product.description,
            }
        }
        else {
            return {
                brand: "",
                name: "",
                category: "",
                price: "",
                weight: "",
                stock: "",
                featured: false,
                description: "",
            }
        }
    })
    const [showError, setShowError] = useState(false)
    const [errorMessage, setErrorMessage] = useState("");

    const [image, setImage] = useState(null)
    const [imagePreview, setImagePreview] = useState(null);

    const navigate = useNavigate()

    const checkLogin = async (e) => {
        if (await checkAdminLoginHelper() == false) {
            navigate('/admin/login')
            console.log("admin login expired")
        }
    }

    const validateNumber = (number) => {
        if (number < 0) {
            return false;
        }
        const newNumber = number.toString().replace(/[^0-9.]/g, ""); 
        if (number != newNumber) {
            return false; //this means there are characters other than 0-9
        }
        const numSplit = newNumber.split("."); {
            if (numSplit.length > 2) {
                return false; //this means there are multiple decimal
            }
        }
        return true;
    }


    const validationInputs = () => {
        if (Object.values(productInfo).some((input) => input === "")) {
            setErrorMessage("Please fill out all input fields")
            setShowError(true)
            return false;
        }
        if (!product && !image) {
            setErrorMessage("Please upload an image")
            setShowError(true)
            return false;
        }
        if (!validateNumber(productInfo.stock)) {
            setErrorMessage("Please enter a valid number for the stock")
            setShowError(true)
            return false;
        }
        if (!validateNumber(productInfo.price)) {
            setErrorMessage("Please enter a valid number for the price")
            setShowError(true)
            return false;
        }
        if (!validateNumber(productInfo.weight)) {
            setErrorMessage("Please enter a valid number for the weight")
            setShowError(true)
            return false;
        }
        setShowError(false);
        return true;
        
    }

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImage(file);
            setImagePreview(URL.createObjectURL(file));
        }
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

    const handleDelete = async (e) => {
        console.log("DELETING")
        e.preventDefault();
        checkLogin();
        try {
            const response = await axios.delete(`http://127.0.0.1:8080/api/admin/products/${product.product_id}`, {
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("admin_access_token")}`
                },
            });
            console.log('Product deleted successfully:', response.data);
            onCancel(); // Close the form after submission (optional)
            window.location.reload();
        } catch (error) {
            if (error.response.data.error) {
                setErrorMessage(error.response.data.error)
                setShowError(true)
            }
            else {
                setErrorMessage("There was an error")
                setShowError(true)
            }
        }

    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        checkLogin();
        if (!validationInputs()) {
            return;
        }
        if (product) {
            const data = {
                product_id: product.product_id,
                brand: productInfo.brand,
                name: productInfo.name,
                category: productInfo.category,
                price: productInfo.price,
                weight: productInfo.weight,
                stock: productInfo.stock,
                featured: productInfo.featured,
                description: productInfo.description,
            };
    
            const imageData = new FormData();
            imageData.append("product_id", product.product_id);
            imageData.append("image", image);
    
            try {
                const response = await axios.put('http://127.0.0.1:8080/api/admin/update-product/', data, {
                    headers: {
                        'Content-Type': 'application/json', 
                        "Authorization": `Bearer ${localStorage.getItem("admin_access_token")}`
                    },
                });
                console.log('Product info updated successfully:', response.data);
                if (image) {
                    const imageResponse = await axios.put('http://127.0.0.1:8080/api/admin/update-image/', imageData, {
                        headers: {
                           'Content-Type': 'multipart/form-data',
                           "Authorization": `Bearer ${localStorage.getItem("admin_access_token")}`
                        },
                    });
                    console.log('Product image updated successfully:', response.data);
                }
                onCancel(); // Close the form after submission (optional)
                window.location.reload();
            } catch (error) {
                if (error.response.data.error) {
                    setErrorMessage(error.response.data.error)
                    setShowError(true)
                }
                else {
                    setErrorMessage("There was an error")
                    setShowError(true)
                }
            }
        }
        else {
            const data = {
                brand: productInfo.brand,
                name: productInfo.name,
                category: productInfo.category,
                price: productInfo.price,
                weight: productInfo.weight,
                stock: productInfo.stock,
                featured: productInfo.featured,
                description: productInfo.description,
            };
    
            const formData = new FormData();
            formData.append("image", image);
            formData.append("data", JSON.stringify(data));
    
            try {
                const response = await axios.post('http://127.0.0.1:8080/api/admin/add-product/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                        'Authorization': `Bearer ${localStorage.getItem("admin_access_token")}`
                    },
                });
                console.log('Product added successfully:', response.data);
                onCancel(); // Close the form after submission (optional)
                window.location.reload();
            } catch (error) {
                console.log(error.response.data.error)
                if (error.response.data.error) {
                    setErrorMessage(error.response.data.error)
                    setShowError(true)
                }
                else {
                    setErrorMessage("There was an error")
                    setShowError(true)
                }
            }
        }
        
        
    }


    return(
        <>
            <form className="product-form" action="POST" onSubmit={handleSubmit} >
                <div className="product-form-image-wrapper">
                    {imagePreview 
                    ? <img src={imagePreview}></img> : product 
                    ? <img src={`http://127.0.0.1:8080/api/image/${product.product_id}`} alt="" /> 
                    : <></>
                    }
                </div>
                <div className="input-wrapper-image">
                    <label htmlFor="image">Upload image:</label>
                    <input type="file" id="image" name="image" accept="image/*" onChange={handleImageChange} />
                </div>
               
            <div className="input-wrapper">
                <label htmlFor="brand">Brand</label>
                <input type="text" id="brand" name="brand" value={productInfo.brand} onChange={updateForm} required />
            </div>
            <div className="input-wrapper">
                <label htmlFor="name">Name</label>
                <input type="text" id="name" name="name" value={productInfo.name} onChange={updateForm} required />
            </div>
            <div className="input-wrapper">
                <label htmlFor="name">Category</label>
                <select id="category" name="category" value={productInfo.category} onChange={updateForm} required>
                    <option value="" disabled>
                    Select a category
                    </option>
                    <option value="Meats">Meats</option>
                    <option value="Produce">Produce</option>
                    <option value="Canned Foods">Canned Foods</option>
                    <option value="Frozen Foods">Frozen Foods</option>
                    <option value="Snacks">Snacks</option>
                    <option value="Drinks">Drinks</option>
                    <option value="Grains">Grains</option>
                    <option value="Ingredients">Ingredients</option>
                    <option value="Baked">Baked</option>
                    <option value="Dairy">Dairy</option>
                </select>
            </div>
            <div className="input-wrapper">
                <label htmlFor="price">Price ($)</label>
                <input type="number" id="price" name="price" value={productInfo.price} onChange={updateForm} required/>
            </div>
            <div className="input-wrapper">
                <label htmlFor="weight">Weight (lbs)</label>
                <input type="number" id="weight" name="weight" value={productInfo.weight} onChange={updateForm} required/>
            </div>
            <div className="input-wrapper">
                <label htmlFor="stock">Stock</label>
                <input type="number" id="stock" name="stock" value={productInfo.stock} onChange={updateForm} required/>
            </div>
            <div className="input-wrapper">
                <label htmlFor="description">Description</label>
                <textarea id="description" name="description" rows="6" value={productInfo.description} onChange={updateForm} required/>
            </div>
            <div className="input-wrapper-featured">
                <label htmlFor="description">Featured</label>
                <input type="checkbox" id="featured" name="featured" value={productInfo.featured} checked={productInfo.featured} onChange={updateForm}/>
            </div>
            <div className="buttons">
                <button type="submit" className="submit-changes" onClick={handleSubmit}> {product ? "Submit Changes" : "Add product"}</button>
                <button className="cancel-product-form" onClick={handleCancel}>Cancel</button>
            </div>
            {product && <button className="delete-product-button" onClick={handleDelete}>DELETE PRODUCT</button> }
            {showError && <div className="product-form-error-message">{errorMessage}</div>}
          
        </form>
        </>
    )
}

export default ProductForm;