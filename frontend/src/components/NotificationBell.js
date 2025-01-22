import React, { useState, useEffect, useCallback } from 'react';
import axiosInstance from '../utils/axios';
import './Navbar.css';

const NotificationBell = () => {
  const [notifications, setNotifications] = useState([]);
  const [showNotifications, setShowNotifications] = useState(false);
  const userId = localStorage.getItem('user_id');

  const fetchNotifications = useCallback(async () => {
    try {
      console.log('Fetching notifications for user:', userId);
      const response = await axiosInstance.get(`/notifications?userId=${userId}`);
      console.log('Notifications response:', response.data);
      setNotifications(response.data);
    } catch (err) {
      console.error('Failed to fetch notifications:', err);
    }
  }, [userId]);

  useEffect(() => {
    if (userId) {
      fetchNotifications();
      const interval = setInterval(fetchNotifications, 30000);
      return () => clearInterval(interval);
    }
  }, [fetchNotifications, userId]);

  const markAsRead = async (notificationId) => {
    try {
      await axiosInstance.post('/notifications/mark-read', {
        notificationId
      });
      fetchNotifications();
    } catch (err) {
      console.error('Failed to mark notification as read:', err);
    }
  };

  const unreadCount = notifications.filter(n => !n.IsRead).length;

  return (
    <div className="notification-container">
      <div 
        className={`notification-bell ${unreadCount > 0 ? 'has-notifications' : ''}`}
        onClick={() => setShowNotifications(!showNotifications)}
      >
        <svg 
          width="24" 
          height="24" 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          strokeWidth="2" 
          strokeLinecap="round" 
          strokeLinejoin="round"
        >
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
          <path d="M13.73 21a2 2 0 0 1-3.46 0" />
        </svg>
      </div>

      {showNotifications && (
        <div className="notification-dropdown">
          <div className="notification-header">
            <h3>Notifications</h3>
            {unreadCount > 0 && (
              <span className="unread-count">{unreadCount} unread</span>
            )}
          </div>
          
          <div className="notification-list">
            {notifications.length > 0 ? (
              notifications.map(notification => (
                <div 
                  key={notification.NotificationID}
                  className={`notification-item ${!notification.IsRead ? 'unread' : ''}`}
                  onClick={() => markAsRead(notification.NotificationID)}
                >
                  <div className="notification-title">{notification.Title}</div>
                  <div className="notification-message">{notification.Message}</div>
                  <div className="notification-date">
                    {new Date(notification.CreatedDate).toLocaleDateString()}
                  </div>
                </div>
              ))
            ) : (
              <div className="no-notifications">
                No notifications yet
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default NotificationBell; 