import { useState, useEffect } from 'react'
import axios from 'axios';
import LandingPage from './components/landing-page/LandingPage'

function App() {
  const [count, setCount] = useState(0)
  const[array, setArray] = useState([]);

  const fetchAPI = async () => {
    const response = await axios.get("http://127.0.0.1:8080/api/users");
    console.log(response.data.users);
    setArray(response.data.users);
  }

  useEffect(() => {
    fetchAPI()
  }, [])

  return (
    <>
      <LandingPage />
    </>
  )
}

export default App
