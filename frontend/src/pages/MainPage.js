import React from 'react';
import { Link } from 'react-router-dom';
import './MainPage.css';
import { FaLightbulb, FaChartBar, FaUsers, FaSync, FaBalanceScale, FaLock, FaShieldAlt } from 'react-icons/fa';

const MainPage = () => {
  return (
    <div className="main-page">
      <header className="header">
        <div className="header-content">
          <h1>
            <span className="currency-symbol">$</span>aldo
          </h1>
          <div className="auth-buttons">
            <Link to="/register" className="signup-button">Sign Up</Link>
            <Link to="/login" className="login-button">Login</Link>
          </div>
        </div>
      </header>

      <div className="content-container">
        <div className="description-section">
          <h2 className="headline">
            Smart finance,<br />
            simplified for<br />
            <span className="highlight">everyone.</span>
          </h2>
          <p className="subheadline">
            Take control of shared expenses, track group spending, and manage finances together - all in one place.
          </p>
          <div className="feature-grid">
            <div className="feature-item">
              <span className="feature-icon">
                <FaLightbulb />
              </span>
              <span>Smart Splitting</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">
                <FaChartBar />
              </span>
              <span>Real-time Tracking</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">
                <FaUsers />
              </span>
              <span>Group Management</span>
            </div>
            <div className="feature-item">
              <span className="feature-icon">
                <FaSync />
              </span>
              <span>Auto Sync</span>
            </div>
          </div>
        </div>

        <div className="main-content-box">
          <div className="demo-container">
            <div className="demo-screen">
              <div className="demo-header">
                <h3>Saldo Review</h3>
              </div>
              <div className="demo-content">
                <div className="demo-transaction">
                  <span className="demo-amount positive">+$50.00</span>
                  <span className="demo-description">Dinner with friends</span>
                </div>
                <div className="demo-transaction">
                  <span className="demo-amount negative">-$25.00</span>
                  <span className="demo-description">Movie tickets</span>
                </div>
                <div className="demo-transaction">
                  <span className="demo-amount positive">+$30.00</span>
                  <span className="demo-description">Groceries split</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="image-section">
          <div className="trust-badges">
            <span>
              <FaLock className="badge-icon" />
              Bank-grade Security
            </span>
          </div>
          <div className="circular-image">
            <FaBalanceScale className="scale-icon" />
          </div>
          <div className="trust-badges">
            <span>
              <FaShieldAlt className="badge-icon" />
              Trusted Platform
            </span>
          </div>
        </div>
      </div>

      <footer className="footer">
        <Link to="/register" className="cta-button">Start Managing Smarter</Link>
      </footer>
    </div>
  );
};

export default MainPage; 