import logo from './logo.svg';
import './App.css';
import './button-1.css';
import React, { useState } from 'react';
import axios from 'axios';

export default function App() {
  const [state, setState] = useState({ url: 'No' });

  function login() {
    axios.get('/login')
  }

  return (
    <div className="Login">
      <header className="Login-header">
        <h1>Welcome to SpotAFriend!</h1>
        <button onClick={login} className="button-1" type="button">Login Through Spotify!</button>
      </header>
    </div>
  );
}