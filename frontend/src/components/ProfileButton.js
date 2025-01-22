import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaBalanceScale } from 'react-icons/fa';
import './ProfileButton.css';

const ProfileButton = () => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate('/profile');
  };

  return (
    <button className="profile-button" onClick={handleClick}>
      <div className="profile-icon-circle">
        <FaBalanceScale className="profile-icon" />
      </div>
    </button>
  );
};

export default ProfileButton; 