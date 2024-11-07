import React, {useState} from 'react'
import axios from 'axios'
import { useNavigate, useLocation } from 'react-router-dom';
import '../SearchPage/SearchPage'


const SearchBar = () => {
    const [input, setInput] = useState("");
    const navigate = useNavigate();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const currentCategory = queryParams.get('category');

    

    const handleEnter = (event) => {
        if (event.key == "Enter") {
            search(event)
        }
    }

    const search = (event) => {
        const searchInput = event.target.value;
        setInput(searchInput);
        if (currentCategory == null) {
            navigate(`/search?q=${searchInput}`);
        }
        else {
            navigate(`/search?q=${searchInput}&category=${currentCategory}`);
        }
        
    }

   



  return (
    <div className="search-bar">
        <input type="text" className="search-input" placeholder="Search Groceries" onChange={(e) => setInput(e.target.value)} onKeyDown={handleEnter} />
        <img src="./src/img/search-icon.png" alt="" className="search-icon" value={input} />
    </div>
  )
}

export default SearchBar