import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import './Dashboard.css';
import Dialog from '../components/Dialog';

const FastIcon = () => (
  <div className="feature-icon fast">
    <svg width="32" height="32" viewBox="0 0 24 24" fill="white">
      <path d="M13 3L4 14h7l-2 7 9-11h-7l2-7z"/>
    </svg>
  </div>
);

const GroupIcon = () => (
  <div className="feature-icon group">
    <svg width="32" height="32" viewBox="0 0 24 24" fill="white">
      <path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"/>
    </svg>
  </div>
);

const TrackIcon = () => (
  <div className="feature-icon track">
    <svg viewBox="0 0 24 24" width="32" height="32" fill="white">
      <path d="M11.8 10.9c-2.27-.59-3-1.2-3-2.15 0-1.09 1.01-1.85 2.7-1.85 1.78 0 2.44.85 2.5 2.1h2.21c-.07-1.72-1.12-3.3-3.21-3.81V3h-3v2.16c-1.94.42-3.5 1.68-3.5 3.61 0 2.31 1.91 3.46 4.7 4.13 2.5.6 3 1.48 3 2.41 0 .69-.49 1.79-2.7 1.79-2.06 0-2.87-.92-2.98-2.1h-2.2c.12 2.19 1.76 3.42 3.68 3.83V21h3v-2.15c1.95-.37 3.5-1.5 3.5-3.55 0-2.84-2.43-3.81-4.7-4.4z"/>
    </svg>
  </div>
);

const Dashboard = () => {
  const [groups, setGroups] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [groupToDelete, setGroupToDelete] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem('token');
      const userId = localStorage.getItem('user_id');

      if (!userId || !token) {
        setError('Unauthorized: Please log in to access the dashboard.');
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get('http://localhost:5005/groups', {
          headers: {
            Authorization: `Bearer ${token}`,
            'User-ID': userId,
          },
        });

        setGroups(response.data);
      } catch (err) {
        setError(err.response?.data?.error || 'Failed to fetch groups.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleDeleteClick = (e, groupId) => {
    e.preventDefault();
    setGroupToDelete(groupId);
    setShowDeleteDialog(true);
  };

  const confirmDeleteGroup = async () => {
    try {
      await axios.delete(`http://localhost:5005/groups/${groupToDelete}`);
      setGroups(groups.filter(group => group.GroupID !== groupToDelete));
      setShowDeleteDialog(false);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete group');
    }
  };

  if (loading) return <div className="loading-state">Loading dashboard...</div>;
  if (error) return <div className="error-state">Error: {error}</div>;

  return (
    <div className="dashboard-container">
      <div className="welcome-section">
        <div className="welcome-content">
          <h1 className="welcome-title">Welcome to Saldo</h1>
          <p className="welcome-subtitle">Track shared expenses, split bills, and manage group finances effortlessly</p>
          <div className="feature-stats">
            <div className="feature-stat">
              <FastIcon />
              <div className="stat-info">
                <h3>Fast & Easy</h3>
                <p>Split bills in seconds</p>
              </div>
            </div>
            <div className="feature-stat">
              <GroupIcon />
              <div className="stat-info">
                <h3>Group Friendly</h3>
                <p>Perfect for roommates & trips</p>
              </div>
            </div>
            <div className="feature-stat">
              <TrackIcon />
              <div className="stat-info">
                <h3>Track Everything</h3>
                <p>Never lose track of shared expenses</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="dashboard-header">
        <h2 className="dashboard-title">Your Groups</h2>
        <Link to="/create-group" className="create-group-button">
          + Create New Group
        </Link>
      </div>

      {groups.length > 0 ? (
        <div className="groups-container">
          {groups.map((group) => (
            <div key={group.GroupID} className="group-card">
              <Link to={`/groups/${group.GroupID}`} className="group-card-content">
                <div className="group-card-header">
                  <h3 className="group-name">{group.GroupName}</h3>
                  <button
                    className="delete-button"
                    onClick={(e) => handleDeleteClick(e, group.GroupID)}
                  >
                    <svg viewBox="0 0 24 24">
                      <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                    </svg>
                  </button>
                </div>
                <p className="group-date">Created on {new Date(group.CreatedDate).toLocaleDateString()}</p>
              </Link>
            </div>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <p>You are not part of any groups yet.</p>
          <p>Create a new group to get started!</p>
        </div>
      )}

      <Dialog
        isOpen={showDeleteDialog}
        message="Are you sure you want to delete this group?"
        onConfirm={confirmDeleteGroup}
        onCancel={() => setShowDeleteDialog(false)}
      />
    </div>
  );
};

export default Dashboard;
