import React, { useState } from "react";
import axios from "axios";
import "./App.css";

export default function App() {
  const [domain, setDomain] = useState("");
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [darkMode, setDarkMode] = useState(true);

  const fetchSSLData = async () => {
    if (!domain.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(
        `https://sslcert-checker.azurewebsites.net/api/get_cert?domain=${domain}`
      );
      setData(response.data);
    } catch (err) {
      setError("Unable to fetch certificate info. Please check the domain.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`app ${darkMode ? "dark" : "light"}`}>
      {/* Header */}
      <header className="header">
        <h1 className="logo">
          SSL<span>Dashboard</span>
        </h1>
        <div className="theme-toggle">
          <label className="switch">
            <input
              type="checkbox"
              checked={darkMode}
              onChange={() => setDarkMode(!darkMode)}
            />
            <span className="slider"></span>
          </label>
          <span>{darkMode ? "Dark" : "Light"}</span>
        </div>
      </header>

      {/* Input Section */}
      <div className="search-section">
        <input
          type="text"
          placeholder="Enter domains (comma-separated)"
          value={domain}
          onChange={(e) => setDomain(e.target.value)}
        />
        <button onClick={fetchSSLData}>Check SSL</button>
      </div>

      {/* Error Message */}
      {error && <div className="error">{error}</div>}

      {/* Loading */}
      {loading && <div className="loading">Fetching SSL details...</div>}

      {/* Cards */}
      <div className="cards">
        {data.map((item, index) => (
          <div className="card" key={index}>
            <h2>{item.domain}</h2>
            <p><strong>CN:</strong> {item.cn || "N/A"}</p>
            <p><strong>Valid From:</strong> {item.valid_from || "N/A"}</p>
            <p><strong>Valid To:</strong> {item.valid_to || "N/A"}</p>
            <span
              className={`status ${
                item.error
                  ? "expired"
                  : item.days_remaining <= 0
                  ? "expired"
                  : item.days_remaining <= 30
                  ? "warning"
                  : "valid"
              }`}
            >
              {item.error
                ? "Expired / Invalid"
                : item.days_remaining <= 0
                ? "Expired"
                : `${item.days_remaining} days left`}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
