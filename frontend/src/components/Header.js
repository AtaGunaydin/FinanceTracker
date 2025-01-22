import React from 'react';
import { Link } from 'react-router-dom';
import '../pages/MainPage.css';

const Header = () => {
  return (
    <header className="header">
      <div className="header-content">
        <h1>
          <img src="/saldo-icon.svg" alt="Saldo" className="header-logo" />
          <span className="currency-symbol">$</span>aldo
        </h1>
        <div className="auth-buttons">
          <Link to="/register" className="signup-button">Sign Up</Link>
          <Link to="/login" className="login-button">Login</Link>
        </div>
      </div>
    </header>
  );
};

export default Header; 