import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dnaSeq, setDnaSeq] = useState('');
  const [protSeq, setProtSeq] = useState('');
  const [go0, setGo0] = useState('');
  const [go1, setGo1] = useState('');
  const [namespace, setNamespace] = useState('');

  const handleError = (errorMessage) => {
    setError(errorMessage);
  };

  const handleClose = () => {
    setError(null);
  };

  function ErrorModal({ error, onClose }) {
  return (
    <div className="modal-overlay">
      <div className="modal">
        <div className="modal-content">
          <span className="close" onClick={onClose}>&times;</span>
          <p>{error}</p>
        </div>
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
        const message = data.message;
        setDnaSeq(message.dna_seq);
        setProtSeq(message.prot_seq);
        setGo0(message.go0);
        setGo1(message.go1);
        setNamespace(message.namespace);
        setQuery('');
      })
      .catch(error => {
        setLoading(false);
        console.error('Error:', error);
        handleError("An error occurred");
      });
  };

  const handleScrollHorizontally = (event) => {
    const container = event.target;
    const delta = Math.max(-1, Math.min(1, (event.deltaY || -event.detail)));
    container.scrollLeft -= delta * 50; // Adjust scrolling speed as needed
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
        {!loading && dnaSeq && (
          <div className="results-container"  onWheel={handleScrollHorizontally}>
            <div className="results">
              <h2>Search Results:</h2>
              <p><strong>DNA Sequence:</strong> {dnaSeq}</p>
              <p><strong>Protein Sequence:</strong> {protSeq}</p>
              <p><strong>GO 0:</strong> {go0}</p>
              <p><strong>GO 1:</strong> {go1}</p>
              <p><strong>Namespace:</strong> {namespace}</p>
            </div>
            <div className="results-end"></div>
            <div className="results-blur"></div>
          </div>
        )}
        {error && <ErrorModal error={error} onClose={handleClose} />}
      </header>
    </div>
  );
}

export default App;
