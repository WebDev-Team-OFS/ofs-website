import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './AuthPages.css';

const AuthPages = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirm_password: '',
    username: '',
    first_name: '',
    last_name: ''
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:8080/api/login', {
        email: formData.email,
        password: formData.password
      }, {
        withCredentials: true
      });

      if (response.data.user) {
        localStorage.setItem('user', JSON.stringify(response.data.user));
        setSuccessMessage('Login successful!');
        setTimeout(() => navigate('/'), 1500);
      }
    } catch (err) {
      console.log(err.response ? err.response.data : err.message);
      setError(err.response?.data?.error || 'An error occurred during login');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    if (formData.password !== formData.confirm_password) {
      setError('Passwords do not match');
      setIsLoading(false);
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:8080/api/register', formData, {
         withCredentials: true, // Include for session-based auth
      });
      
      if (response.status === 201) {
        setSuccessMessage('Registration successful! Please login.');
        setTimeout(() => {
          setIsLogin(true);
          setFormData({
            email: '',
            password: '',
            confirm_password: '',
            username: '',
            first_name: '',
            last_name: ''
          });
          setSuccessMessage('');
        }, 1500);
      }
    } catch (err) {
      console.log(err.response ? err.response.data : err.message);
      setError(err.response?.data?.error || 'An error occurred during registration');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h2 className="auth-title">
          {isLogin ? 'Sign in to your account' : 'Create new account'}
        </h2>
        
        {error && <div className="auth-error">{error}</div>}
        {successMessage && <div className="auth-success">{successMessage}</div>}

        <form onSubmit={isLogin ? handleLogin : handleRegister} className="auth-form">
          <div>
            <label className="auth-label">Email address</label>
            <input
              type="email"
              name="email"
              required
              value={formData.email}
              onChange={handleInputChange}
              className="auth-input"
              placeholder="Enter your email"
            />
          </div>

          {!isLogin && (
            <>
              <div>
                <label className="auth-label">Username</label>
                <input
                  type="text"
                  name="username"
                  required
                  value={formData.username}
                  onChange={handleInputChange}
                  className="auth-input"
                  placeholder="Choose a username"
                />
              </div>
              <div className="auth-row">
                <div>
                  <label className="auth-label">First Name</label>
                  <input
                    type="text"
                    name="first_name"
                    required
                    value={formData.first_name}
                    onChange={handleInputChange}
                    className="auth-input"
                    placeholder="First name"
                  />
                </div>
                <div>
                  <label className="auth-label">Last Name</label>
                  <input
                    type="text"
                    name="last_name"
                    required
                    value={formData.last_name}
                    onChange={handleInputChange}
                    className="auth-input"
                    placeholder="Last name"
                  />
                </div>
              </div>
            </>
          )}

          <div>
            <label className="auth-label">Password</label>
            <input
              type="password"
              name="password"
              required
              value={formData.password}
              onChange={handleInputChange}
              className="auth-input"
              placeholder="Enter your password"
            />
          </div>

          {!isLogin && (
            <div>
              <label className="auth-label">Confirm Password</label>
              <input
                type="password"
                name="confirm_password"
                required
                value={formData.confirm_password}
                onChange={handleInputChange}
                className="auth-input"
                placeholder="Confirm your password"
              />
            </div>
          )}

          <button type="submit" disabled={isLoading} className="auth-button">
            {isLoading ? 'Processing...' : isLogin ? 'Sign in' : 'Create Account'}
          </button>
        </form>

        <div className="auth-toggle">
          <button onClick={() => setIsLogin(!isLogin)} className="auth-link">
            {isLogin ? "Don't have an account? Sign up" : "Already have an account? Sign in"}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AuthPages;
