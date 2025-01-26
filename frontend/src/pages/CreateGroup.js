import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { FaBalanceScale } from 'react-icons/fa';
import './CreateGroup.css';
import DOMPurify from 'dompurify';

const CreateGroup = () => {
  const navigate = useNavigate();
  const [groupName, setGroupName] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [message, setMessage] = useState('');
  const [isError, setIsError] = useState(false);
  const [errors, setErrors] = useState({
    groupName: '',
    members: ''
  });

  const sanitizeInput = (input) => {
    const cleanInput = DOMPurify.sanitize(input, {
      ALLOWED_TAGS: [], 
      ALLOWED_ATTR: [] 
    });
    
    return cleanInput.replace(/[^a-zA-Z0-9\s\-_]/g, '');
  };

  const handleGroupNameChange = (e) => {
    const rawValue = e.target.value;
    const sanitizedValue = sanitizeInput(e.target.value);
    console.log('Raw input:', rawValue);
    console.log('Sanitized input:', sanitizedValue);
    setGroupName(sanitizedValue);
  };

  const handleSearchChange = (e) => {
    const sanitizedValue = sanitizeInput(e.target.value);
    setSearchTerm(sanitizedValue);
  };

  const searchUsers = async (term) => {
    if (term.length < 2) {
      setSearchResults([]);
      return;
    }

    try {
      const response = await axios.get(`http://localhost:5005/users/search?term=${term}`, {
        headers: {
          'User-ID': localStorage.getItem('user_id')
        }
      });
      
      setSearchResults(response.data);
    } catch (err) {
      console.error('Search error:', err);
      if (err.response?.status === 401) {
        setMessage('Please log in to search users');
        setIsError(true);
      }
    }
  };

  const toggleUser = (user) => {
    if (selectedUsers.find(u => u.UserID === user.UserID)) {
      setSelectedUsers(selectedUsers.filter(u => u.UserID !== user.UserID));
    } else {
      setSelectedUsers([...selectedUsers, user]);
    }
  };

  const validateGroupName = (name) => {
    if (!name.trim()) {
      return 'Group name is required';
    }
    if (name.length < 3) {
      return 'Group name must be at least 3 characters';
    }
    if (name.length > 50) {
      return 'Group name cannot exceed 50 characters';
    }
    return '';
  };

  const validateMembers = (members) => {
    if (members.length === 0) {
      return 'Please add at least one member';
    }
    if (members.length > 10) {
      return 'Maximum 10 members allowed';
    }
    return '';
  };

  const handleCreateGroup = async (e) => {
    e.preventDefault();
    
    const groupNameError = validateGroupName(groupName);
    const membersError = validateMembers(selectedUsers);

    setErrors({
      groupName: groupNameError,
      members: membersError
    });

    if (groupNameError || membersError) {
      return;
    }

    try {
      await axios.post(
        'http://localhost:5005/groups',
        { 
          GroupName: groupName,
          Members: selectedUsers.map(user => user.UserID)
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'User-ID': localStorage.getItem('user_id')
          }
        }
      );

      setMessage('Group created successfully!');
      setIsError(false);
      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);
    } catch (err) {
      setMessage(err.response?.data?.error || 'Failed to create group.');
      setIsError(true);
    }
  };

  useEffect(() => {
    const delaySearch = setTimeout(() => {
      if (searchTerm) {
        searchUsers(searchTerm);
      }
    }, 300);

    return () => clearTimeout(delaySearch);
  }, [searchTerm]);

  return (
    <div className="create-group-container">
      <div className="create-group-card">
        <h2 className="create-group-title">Create New Group</h2>
        <form onSubmit={handleCreateGroup} className="create-group-form">
          <div className="form-group">
            <label>Group Name</label>
            <input
              type="text"
              value={groupName}
              onChange={handleGroupNameChange}
              placeholder="Enter group name"
              maxLength={50}
              required
              className={errors.groupName ? 'error' : ''}
            />
            {errors.groupName && (
              <span className="error-message">{errors.groupName}</span>
            )}
          </div>

          <div className="form-group">
            <label>Add Members</label>
            <input
              type="text"
              value={searchTerm}
              onChange={handleSearchChange}
              placeholder="Search users by name or email"
              maxLength={100}
              className="search-input"
            />
            
            {searchResults.length > 0 ? (
              <div className="search-results">
                {searchResults.map(user => (
                  <div 
                    key={user.UserID} 
                    className={`search-result-item ${
                      selectedUsers.find(u => u.UserID === user.UserID) ? 'selected' : ''
                    }`}
                    onClick={() => toggleUser(user)}
                  >
                    <div className="user-info">
                      <span className="user-name">{user.Name}</span>
                      <span className="user-email">{user.Email}</span>
                    </div>
                    <button 
                      type="button"
                      className={`add-user-btn ${
                        selectedUsers.find(u => u.UserID === user.UserID) ? 'selected' : ''
                      }`}
                    >
                      {selectedUsers.find(u => u.UserID === user.UserID) ? '✓' : '+'}
                    </button>
                  </div>
                ))}
              </div>
            ) : searchTerm.length >= 2 ? (
              <div className="no-results">No users found</div>
            ) : null}

            {selectedUsers.length > 0 && (
              <div className="selected-users">
                <h4>Selected Members:</h4>
                {selectedUsers.map(user => (
                  <div key={user.UserID} className="selected-user-tag">
                    {user.Name}
                    <button 
                      type="button" 
                      onClick={() => toggleUser(user)}
                      className="remove-user"
                    >
                      ×
                    </button>
                  </div>
                ))}
              </div>
            )}
            {errors.members && (
              <span className="error-message">{errors.members}</span>
            )}
          </div>

          <button type="submit" className="submit-button">
            Create Group
          </button>
        </form>

        {message && (
          <div className={`message ${isError ? 'error-message' : 'success-message'}`}>
            {message}
          </div>
        )}
      </div>
      
      <div className="create-group-info-section">
        <div className="create-group-balance-icon">
          <FaBalanceScale />
        </div>
        <h2>Start Managing Your Group Expenses</h2>
        <p>Create a group, add members, and start tracking shared expenses effortlessly.</p>
      </div>
    </div>
  );
};

export default CreateGroup;
