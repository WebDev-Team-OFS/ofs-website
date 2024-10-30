import React, {useState, useEffect} from 'react'
import axios from 'axios'


const SearchBar = () => {
    const [input, setInput] = useState("");

    const handleEnter = (event) => {
        if (event.key == "Enter") {
            search(event)
        }
    }

    const search = (event) => {
        const searchInput = event.target.value;
        setInput(searchInput);
        fetchData(searchInput);
    }

    const fetchData = async (searchInput) => {
        const response = await axios.get(`http://127.0.0.1:8080/api/search?query=${searchInput}`);
        console.log(response.data);
      }



  return (
    <div className="search-bar">
        <input type="text" className="search-input" placeholder="Search Groceries" onChange={(e) => setInput(e.target.value)} onKeyDown={handleEnter} />
        <img src="./src/img/search-icon.png" alt="" className="search-icon" value={input} />
    </div>
  )
}

export default SearchBar