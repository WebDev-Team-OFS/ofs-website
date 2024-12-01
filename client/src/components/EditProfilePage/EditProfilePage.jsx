import React from "react";
import "./editprofile-page.css";

const EditProfile = () => {
  const user = {
    fullName: "Monkey D. Luffy",
    birthday: "",
    email: "monkeydluffy@gmail.com",
    emailVerified: true,
    primaryNumber: "(123) 456-7890",
    primaryNumberVerified: true,
    contactNumber: "",
    password: "",
    clubCardNumber: "49596739072",
  };

  return (
    <div className="edit-profile-page">
      <h1>Edit Profile</h1>
      <div className="profile-sections">
        {/* Full Name */}
        <div className="profile-row">
          <span className="label">Full name</span>
          <span className="value">{user.fullName || "Empty"}</span>
          <button className="edit-btn">Edit</button>
        </div>

        {/* Birthday */}
        <div className="profile-row">
          <span className="label">Birthday</span>
          <span className="value">{user.birthday || "Empty"}</span>
          <button className="add-btn">Add</button>
        </div>

        {/* Email Address */}
        <div className="profile-row">
          <span className="label">Email address</span>
          <span className="value">{user.email}</span>
          <span className="status">
            {user.emailVerified ? "✔ Verified" : "Not Verified"}
          </span>
          <button className="edit-btn">Edit</button>
        </div>

        {/* Primary Number */}
        <div className="profile-row">
          <span className="label">Primary number (mobile)</span>
          <span className="value">{user.primaryNumber || "Empty"}</span>
          <span className="status">
            {user.primaryNumberVerified ? "✔ Verified" : "Not Verified"}
          </span>
          <button className="edit-btn">Edit</button>
        </div>

        {/* Contact Number */}
        <div className="profile-row">
          <span className="label">Contact number</span>
          <span className="value">{user.contactNumber || "Empty"}</span>
          <button className="add-btn">Add</button>
        </div>

        {/* Password */}
        <div className="profile-row">
          <span className="label">Password</span>
          <span className="value">{user.password || "Empty"}</span>
          <button className="add-btn">Add</button>
        </div>

        {/* Club Card Number */}
        <div className="profile-row">
          <span className="label">Club Card number</span>
          <span className="value">{user.clubCardNumber || "Empty"}</span>
        </div>
      </div>
    </div>
  );
};

export default EditProfile;
