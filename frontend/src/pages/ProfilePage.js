import React, { useState, useEffect } from 'react';
import { FaUser, FaEnvelope, FaLock } from 'react-icons/fa';
import axiosInstance from '../utils/axios';
import './ProfilePage.css';
import { validatePassword } from '../utils/passwordValidator';

const ProfilePage = () => {
  const [user, setUser] = useState({
    name: '',
    email: '',
  });
  const [isChangingPassword, setIsChangingPassword] = useState(false);
  const [passwordForm, setPasswordForm] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  });
  const [message, setMessage] = useState({ text: '', type: '' });

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const userId = localStorage.getItem('user_id');
        if (!userId) {
          setMessage({ text: 'Please login to view profile', type: 'error' });
          return;
        }

        const response = await axiosInstance.get(`/users/${userId}`);

        if (response.data) {
          setUser({
            name: response.data.Name,
            email: response.data.Email
          });
        }
      } catch (error) {
        setMessage({ 
          text: error.response?.data?.error || 'Failed to load profile data', 
          type: 'error' 
        });
      }
    };

    fetchUserData();
  }, []);

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    
    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      setMessage({ text: 'Passwords do not match', type: 'error' });
      return;
    }

    const passwordErrors = validatePassword(passwordForm.newPassword);
    if (passwordErrors.length > 0) {
      setMessage({ text: passwordErrors[0], type: 'error' });
      return;
    }

    try {
      const userId = localStorage.getItem('user_id');
      const response = await axiosInstance.put(
        `/users/${userId}/password`,
        {
          currentPassword: passwordForm.currentPassword,
          newPassword: passwordForm.newPassword
        }
      );

      if (response.status === 200) {
        setMessage({ text: 'Password updated successfully', type: 'success' });
        setIsChangingPassword(false);
        setPasswordForm({
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        });
      }
    } catch (error) {
      setMessage({ 
        text: error.response?.data?.error || 'Failed to update password', 
        type: 'error' 
      });
    }
  };

  return (
    <div className="profile-page">
      <div className="profile-container">
        <h1>Profile Settings</h1>
        
        <div className="profile-section">
          <div className="profile-info">
            <div className="info-item">
              <FaUser className="info-icon" />
              <div className="info-content">
                <label>Name</label>
                <span>{user.name || 'Loading...'}</span>
              </div>
            </div>
            
            <div className="info-item">
              <FaEnvelope className="info-icon" />
              <div className="info-content">
                <label>Email</label>
                <span>{user.email || 'Loading...'}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="profile-section">
          <h2>Security</h2>
          {!isChangingPassword ? (
            <button 
              className="change-password-button"
              onClick={() => setIsChangingPassword(true)}
            >
              <FaLock className="button-icon" />
              Change Password
            </button>
          ) : (
            <form className="password-form" onSubmit={handlePasswordChange}>
              <div className="form-group">
                <input
                  type="password"
                  placeholder="Current Password"
                  value={passwordForm.currentPassword}
                  onChange={(e) => setPasswordForm({
                    ...passwordForm,
                    currentPassword: e.target.value
                  })}
                  required
                />
              </div>
              <div className="form-group">
                <input
                  type="password"
                  placeholder="New Password"
                  value={passwordForm.newPassword}
                  onChange={(e) => setPasswordForm({
                    ...passwordForm,
                    newPassword: e.target.value
                  })}
                  required
                />
                <small className="password-requirements">
                  Password must:
                  <ul>
                    <li>Be at least 8 characters long</li>
                    <li>Contain at least one uppercase letter</li>
                    <li>Contain at least one lowercase letter</li>
                    <li>Contain at least one number</li>
                    <li>Contain at least one special character</li>
                  </ul>
                </small>
              </div>
              <div className="form-group">
                <input
                  type="password"
                  placeholder="Confirm New Password"
                  value={passwordForm.confirmPassword}
                  onChange={(e) => setPasswordForm({
                    ...passwordForm,
                    confirmPassword: e.target.value
                  })}
                  required
                />
              </div>
              <div className="form-actions">
                <button type="submit" className="save-button">
                  Save Changes
                </button>
                <button 
                  type="button" 
                  className="cancel-button"
                  onClick={() => setIsChangingPassword(false)}
                >
                  Cancel
                </button>
              </div>
            </form>
          )}
        </div>

        {message.text && (
          <div className={`message ${message.type}`}>
            {message.text}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProfilePage; 