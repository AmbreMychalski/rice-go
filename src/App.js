import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null); 

  const handleError = (errorMessage) => {
    setError(errorMessage);
  };
  const handleClose = () => {
    setError(null);
  };

  function ErrorModal({ error, onClose }) {
    return (
      <div className="modal">
        <div className="modal-content">
          <span className="close" onClick={onClose}>&times;</span>
          <p>{error}</p>
        </div>
      </div>
    );
  }
  
  const handleSearchChange = (event) => {
    setQuery(event.target.value);
  };

  const handleSearchSubmit = (event) => {
    setLoading(true);
    event.preventDefault();

    fetch('http://localhost:3001/api/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: query }),
    })
      .then(response => response.json())
      .then(data => {
        setLoading(false);
        setResults(data.message);
        console.log(data)
      })
      .catch(error => {
        setLoading(false);
        console.error('Error:', error);
      });
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>GO-Rice</h1>
        <form onSubmit={handleSearchSubmit}>
          <input
            type="text"
            value={query}
            onChange={handleSearchChange}
            placeholder="Search..."
            className="search-bar"
          />
          <button type="submit" className="search-button">Search</button>
        </form>
        {loading && <p>Loading...</p>}
        {results && <div className="results">
          <h2>Search Results:</h2>
          <p>{results}</p>
        </div>}
      </header>
    </div>
  );
}

export default App;
