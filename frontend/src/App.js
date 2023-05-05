import logo from './logo.svg';
import './App.css';
import './button-1.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Routes, Link, Outlet, Navigate, useNavigate } from 'react-router-dom';

function login() {
  axios.get('/login', { withCredentials: true })
    .then(response => {
      // save the session cookie in the browser
      console.log('response from login', response);
    })
    .catch(error => {
      console.log(error);
    });
}

function LoginPage({ onLogin }) {
  return (
    <div className="Login">
      <header className="Login-header">
        <h1>Welcome to SpotAFriend!</h1>
        <button onClick={login} className="button-1" type="button">
          Login Through Spotify!
        </button>
      </header>
    </div>
  );
}

function HomePage() {
  const sliderData = ["50 Cent", "Kendrick Lamar", "J Cole", "Bad Bunny", "Metallica"];
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate('/third-page');
  };
  
  const [name, setName] = useState("");

  useEffect(() => {
    axios.get('/getMyID', { withCredentials: true })
      .then(response => {
        setName(response.data);
      })
      .catch(error => {
        console.log(error);
      });
  }, []);

  return (
    <div className="HomePage-background">
      <h1 className="HomePage-header">Welcome {name}</h1>

      <div className="Data-section">
        <p>Your top tune of the day:</p>
        <div className="Data-box">
          <p>The Nights</p>
        </div>
      </div>

      <div className="Top5-section">
        <p>Here are your top 5 artists</p>
        <div className="Slider-container">
          {sliderData.map((item, index) => (
            <div className="Slider-item" key={index}>
              <p>{item}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="Button-container">
        <button className="White-button" onClick={handleButtonClick}>Make-A-Mix</button>
        <button className="White-button">Verse Generator</button>
      </div>
    </div>
  );
}

function ThirdPage() {
  return (
    <div className="HomePage-background">
      <h1>Search For Spotify</h1>
    </div>
  );
}

export default function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  const handleLogin = () => {
    setLoggedIn(true);
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={loggedIn ? <Navigate to="/home" /> : <LoginPage onLogin={handleLogin} />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/third-page" element={<ThirdPage />} />
      </Routes>
    </Router>
  );
}