import React, { useEffect } from 'react';
import './Dialog.css';

const Dialog = ({ isOpen, message, onConfirm, onCancel }) => {
  useEffect(() => {
    // Dialog açıkken arka planı scroll edilemez yap
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="dialog-overlay" onClick={onCancel}>
      <div 
        className="dialog-content" 
        onClick={e => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
        <div className="dialog-header">
          <h3 className="dialog-title">{message}</h3>
        </div>
        <div className="dialog-buttons">
          <button 
            className="dialog-button cancel-button" 
            onClick={onCancel}
          >
            Cancel
          </button>
          <button 
            className="dialog-button confirm-button" 
            onClick={onConfirm}
          >
            OK
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dialog; 