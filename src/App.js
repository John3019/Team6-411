import React, { useState } from 'react';
import Slider from './Slider';
import './App.css';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const items = [
    'Variable 1',
    'Variable 2',
    'Variable 3',
    'Variable 4',
    'Variable 5',
    'Variable 6',
    'Variable 7',
    'Variable 8',
  ];

  const handleLogin = () => {
    setLoggedIn(true);
  };

  const handleLogout = () => {
    setLoggedIn(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Simple Login App</h1>
      </header>
      <main>
        {loggedIn ? (
          <>
            <p>Welcome, user! You are logged in.</p>
            <button onClick={handleLogout}>Log out</button>
            <h2>Pre-existing Variables:</h2>
            <Slider items={items} />
          </>
        ) : (
          <>
            <p>Please log in to access the content.</p>
            <button onClick={handleLogin}>Log in</button>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
