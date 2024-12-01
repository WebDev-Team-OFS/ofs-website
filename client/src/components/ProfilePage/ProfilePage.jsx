import React from "react";
import { useNavigate } from "react-router-dom";
import "./profile-page.css";

const ProfilePage = () => {
  const navigate = useNavigate();

  const user = {
    name: "Monkey D. Luffy",
    email: "monkeydluffy@example.com",
    phone: "123-456-7890",
    address: "123 Wano, New World 19135 ",
  };

  const handleEdit = () => {
    navigate("/edit-profile");
  };

  return (
    <div className="profile-page">
      {/* Header Section */}
      <header className="profile-header">
        <h1>Welcome, {user.name}</h1>
      </header>

      {/* Main Content Section */}
      <div className="profile-content">
        <section className="profile-info">
          <h2>Your Information</h2>
          <p>
            <strong>Name:</strong> {user.name}
          </p>
          <p>
            <strong>Email:</strong> {user.email}
          </p>
          <p>
            <strong>Phone:</strong> {user.phone}
          </p>
          <p>
            <strong>Address:</strong> {user.address}
          </p>
          <button className="edit-btn" onClick={handleEdit}>
            Edit Profile
          </button>
        </section>

        {/* Navigation Links */}
        <nav className="profile-nav">
          <h2>Quick Links</h2>
          <ul>
            <li>
              <a href="#">Purchases</a>
            </li>
            <li>
              <a href="#">Wallet</a>
            </li>
            <li>
              <a href="#">Help</a>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
};

export default ProfilePage;
