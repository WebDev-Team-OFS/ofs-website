import React, {useState} from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom';


const SearchBar = () => {
    const [input, setInput] = useState("");
    const navigate = useNavigate();
    

    const handleEnter = (event) => {
        if (event.key == "Enter") {
            search(event)
        }
    }

    const search = (event) => {
        const searchInput = event.target.value;
        setInput(searchInput);
        navigate(`/search?q=${searchInput}`);
    }

   



  return (
    <div className="search-bar">
        <input type="text" className="search-input" placeholder="Search Groceries" onChange={(e) => setInput(e.target.value)} onKeyDown={handleEnter} />
        <img src="./src/img/search-icon.png" alt="" className="search-icon" value={input} />
    </div>
  )
}

export default SearchBar