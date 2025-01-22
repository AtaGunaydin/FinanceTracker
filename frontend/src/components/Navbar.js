import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import './Navbar.css';
import NotificationBell from './NotificationBell';
import ProfileButton from './ProfileButton';

const Navbar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const isAuthenticated = localStorage.getItem('token');
  
  if (location.pathname === '/') {
    return null;
  }

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_id');
    navigate('/login');
  };

  return (
    <nav className="app-navbar">
      <div className="navbar-content">
        <Link to="/" className="navbar-brand">
          <span className="brand-symbol">$</span>aldo
        </Link>
        
        <div className="navbar-links">
          {isAuthenticated ? (
            <>
              <Link to="/dashboard" className="nav-link">Dashboard</Link>
              <Link to="/create-group" className="nav-link">Create Group</Link>
              <div className="nav-actions">
                <NotificationBell />
                <ProfileButton />
              </div>
              <button onClick={handleLogout} className="logout-button">
                Logout
              </button>
            </>
          ) : (
            <div className="auth-nav">
              <Link to="/login" className="nav-link">Login</Link>
              <Link to="/register" className="nav-button">Sign Up</Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;