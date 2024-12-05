import {useState, useEffect} from "react";
import { useNavigate } from "react-router-dom";
import "./profile-page.css";
import axios from "axios";
import { checkLoginHelper } from "../utils";

const ProfilePage = () => {
  const navigate = useNavigate();

  const [userInfo, setUserInfo] = useState(["", "", "", "", "", "", ""]);
  const [pastTransactions, setPastTransactions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

    const getPastTransactions = async () => {
        if (await checkLoginHelper()) {
            try {
                const response = await axios.get('http://127.0.0.1:8080/api/past_transactions', {
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("access_token")}`
                    }  
                });
                console.log("Past transactions retrieved");
                console.log(response.data.transactions);
                setPastTransactions(response.data.transactions)
                console.log(pastTransactions[0].order_date)
            }
            catch {
                console.log("Past transactions not recieved")
            }
        }
        else {
            console.log("user is not logged in")
        }
    }
    const getUserInfo = async () => {
        if (await checkLoginHelper()) {
            try {
                const response = await axios.get('http://127.0.0.1:8080/api/profile', {
                    headers: {
                        "Authorization": `Bearer ${localStorage.getItem("access_token")}`
                    }  
                });
                console.log("User info retrieved");
                console.log(response.data.profile);
                console.log("hello")
                setUserInfo(response.data.profile)
                console.log(userInfo);
            }
            catch {
                console.log("User info not retrieved")
            }
        }
        else {
            console.log("User is not logged in")
        }
    }

  const handleEdit = () => {
    navigate("/edit-profile");
  };

  useEffect(()=>{
    const fetchData = async () => {
        await getUserInfo();
        await getPastTransactions();
     // Data fetch complete
        setIsLoading(false)
    };
    fetchData();
  }, [])
  if (isLoading) {
    return <div>Loading...</div>
  }

  return (
    <div className="profile-page">
      {/* Header Section */}
      <header className="profile-header">
        <h1>Welcome, {userInfo.first_name + " " + userInfo.last_name + "!"}</h1>
      </header>

      {/* Main Content Section */}
      <div className="profile-content">
        <section className="profile-info">
          <h2>Your Information</h2>
          <p>
            <strong> First Name:</strong> {userInfo.first_name}
          </p>
          <p>
            <strong> Last Name:</strong> {userInfo.last_name}
          </p>
          <p>
            <strong>Email:</strong> {userInfo.email}
          </p>
        </section>
      </div>
      <div className="profile-content">
        <section className="profile-info">
          <h2>Past Transactions</h2>
          {pastTransactions.map((order => (
            <div key={order.order_id}>
                <p>
                <strong> Ordered on </strong> {Date(order.order_date)}
                </p>
                <p>
                <strong>Total Price:</strong> ${order.total_price}
                </p>
                <p className="order-end">
                <strong>Total Weight:</strong> {order.total_weight} lbs
                </p>
            </div>
          )))}
        </section>
      </div>
    </div>
  );
};

export default ProfilePage;