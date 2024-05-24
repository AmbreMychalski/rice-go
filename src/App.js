import React, { useState } from 'react';
import './App.css';

function App() {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
    alert(`Searching for: ${searchTerm}`);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>GO-Rice</h1>
        <form onSubmit={handleSearchSubmit}>
          <input
            type="text"
            value={searchTerm}
            onChange={handleSearchChange}
            placeholder="Search..."
            className="search-bar"
          />
          <button type="submit" className="search-button">Search</button>
        </form>
      </header>
    </div>
  );
}

export default App;
