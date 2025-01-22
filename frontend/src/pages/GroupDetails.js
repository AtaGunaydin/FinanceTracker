import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './GroupDetails.css';
import Dialog from '../components/Dialog';
import { FaBalanceScale, FaTrash } from 'react-icons/fa';

const GroupDetails = () => {
  const { groupId } = useParams();
  const navigate = useNavigate();
  const [group, setGroup] = useState(null);
  const [members, setMembers] = useState([]);
  const [debts, setDebts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showAddDebtModal, setShowAddDebtModal] = useState(false);
  const [newExpense, setNewExpense] = useState({
    paidByUserId: '',
    amount: '',
    description: '',
    splitEqually: true
  });
  const [debtSummary, setDebtSummary] = useState([]);
  const [debtRelations, setDebtRelations] = useState([]);
  const [showDialog, setShowDialog] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [debtToDelete, setDebtToDelete] = useState(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  useEffect(() => {
    const fetchGroupDetails = async () => {
      try {
        // Grup bilgilerini al
        const groupResponse = await axios.get(`http://localhost:5005/groups/${groupId}`);
        setGroup(groupResponse.data);

        // Grup üyelerini al
        const membersResponse = await axios.get(`http://localhost:5005/groups/${groupId}/members`);
        setMembers(membersResponse.data);

        // Grup borçlarını al
        const debtsResponse = await axios.get(`http://localhost:5005/groups/${groupId}/debts`);
        setDebts(debtsResponse.data);

        setLoading(false);
      } catch (err) {
        setError(err.response?.data?.error || 'Failed to fetch group details');
        setLoading(false);
      }
    };

    fetchGroupDetails();
  }, [groupId]);

  useEffect(() => {
    // Borç özetini hesapla
    const calculateDebtSummary = () => {
      const summary = {};
      
      // Her üye için boş özet oluştur
      members.forEach(member => {
        summary[member.UserID] = {
          name: member.Name,
          totalOwed: 0,    // başkalarına olan borç
          totalOwes: 0     // başkalarından alacak
        };
      });

      // Borçları hesapla
      debts.forEach(debt => {
        const amount = parseFloat(debt.Amount);
        summary[debt.FromUserID].totalOwed += amount;  // borçlu
        summary[debt.ToUserID].totalOwes += amount;    // alacaklı
      });

      // Array'e çevir ve net borç durumunu hesapla
      const summaryArray = Object.values(summary).map(item => ({
        ...item,
        netBalance: item.totalOwes - item.totalOwed // pozitif = alacaklı, negatif = borçlu
      }));

      setDebtSummary(summaryArray);
    };

    if (members.length > 0 && debts.length > 0) {
      calculateDebtSummary();
    }
  }, [members, debts]);

  useEffect(() => {
    // Borç ilişkilerini hesapla
    const calculateDebtRelations = () => {
      const relations = {};
      
      debts.forEach(debt => {
        if (debt.Status !== 'paid') {  // Sadece ödenmemiş borçları göster
          const key = `${debt.FromUserID}-${debt.ToUserID}`;
          if (!relations[key]) {
            relations[key] = {
              fromUser: debt.FromUserName,
              toUser: debt.ToUserName,
              totalAmount: 0,
              debtId: debt.DebtID,  // İlk borç ID'sini sakla
              status: debt.Status
            };
          }
          relations[key].totalAmount += parseFloat(debt.Amount);
        }
      });

      // Object'i array'e çevir
      const relationsArray = Object.values(relations).filter(rel => rel.totalAmount > 0);
      setDebtRelations(relationsArray);
    };

    if (debts.length > 0) {
      calculateDebtRelations();
    }
  }, [debts]);

  const handleAddExpense = async (e) => {
    e.preventDefault();
    try {
      const amount = parseFloat(newExpense.amount);
      const splitAmount = amount / (members.length);
      
      // Ödemeyi yapan kişi hariç herkese borç ekle
      const debtPromises = members
        .filter(member => member.UserID !== parseInt(newExpense.paidByUserId))
        .map(member => {
          return axios.post(`http://localhost:5005/groups/${groupId}/debts`, {
            fromUserId: member.UserID,
            toUserId: newExpense.paidByUserId,
            amount: splitAmount.toFixed(2),
            description: newExpense.description,
            status: 'pending'
          });
        });

      await Promise.all(debtPromises);
      
      setShowAddDebtModal(false);
      // Borçları yeniden yükle
      const debtsResponse = await axios.get(`http://localhost:5005/groups/${groupId}/debts`);
      setDebts(debtsResponse.data);
      
      // Formu sıfırla
      setNewExpense({
        paidByUserId: '',
        amount: '',
        description: '',
        splitEqually: true
      });
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to add expense');
    }
  };

  const handleDeleteDebt = (debtId) => {
    setDebtToDelete(debtId);
    setShowDeleteDialog(true);
  };

  const confirmDeleteDebt = async () => {
    try {
      await axios.delete(`http://localhost:5005/groups/${groupId}/debts/${debtToDelete}`);
      setDebts(debts.filter(debt => debt.DebtID !== debtToDelete));
      setShowDeleteDialog(false);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete debt');
    }
  };

  const handleMarkPaid = async (debtId) => {
    try {
      await axios.put(`http://localhost:5005/groups/${groupId}/debts/${debtId}/mark-paid`);
      // Borçları yeniden yükle
      const debtsResponse = await axios.get(`http://localhost:5005/groups/${groupId}/debts`);
      setDebts(debtsResponse.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to mark debt as paid');
    }
  };

  const handleDeleteClick = () => {
    setShowDeleteModal(true);
  };

  const handleConfirmDelete = async () => {
    try {
      await axios.delete(`http://localhost:5005/groups/${groupId}`);
      navigate('/dashboard');
    } catch (error) {
      setError('Failed to delete group');
    }
  };

  if (loading) return <div className="loading-state">Loading group details...</div>;
  if (error) return <div className="error-state">Error: {error}</div>;
  if (!group) return <div className="error-state">Group not found</div>;

  return (
    <div className="group-details-container">
      <div className="group-header">
        <h1 className="group-title">{group.GroupName}</h1>
      </div>

      <div className="group-content">
        <div className="main-content">
          <div className="members-section">
            <h2>Group Members</h2>
            <div className="debt-summary">
              {debtSummary.map(member => (
                <div key={member.name} className="summary-card">
                  <div className="summary-header">
                    <span className="member-name">{member.name}</span>
                    <span className={`net-balance ${member.netBalance >= 0 ? 'positive' : 'negative'}`}>
                      {member.netBalance >= 0 ? '+' : ''}{member.netBalance.toFixed(2)}$
                    </span>
                  </div>
                  <div className="summary-details">
                    <div className="summary-row">
                      <span>Owes:</span>
                      <span className="negative">-{member.totalOwed.toFixed(2)}$</span>
                    </div>
                    <div className="summary-row">
                      <span>Receives:</span>
                      <span className="positive">+{member.totalOwes.toFixed(2)}$</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="debts-section">
            <div className="debts-header">
              <h2>Debts Overview</h2>
              <button 
                className="add-debt-button"
                onClick={() => setShowAddDebtModal(true)}
              >
                + Add Group Expense
              </button>
            </div>
            {debts.length > 0 ? (
              <div className="debts-list">
                {debts.map(debt => (
                  <div key={debt.DebtID} className={`debt-card ${debt.Status === 'paid' ? 'paid' : ''}`}>
                    <div className="debt-amount-section">
                      <span className="debt-amount">${parseFloat(debt.Amount).toFixed(2)}</span>
                      {debt.Status === 'paid' && <span className="paid-badge">PAID</span>}
                    </div>
                    <div className="debt-info-section">
                      <div className="debt-users">
                        <span className="user from-user">{debt.FromUserName}</span>
                        <span className="arrow">→</span>
                        <span className="user to-user">{debt.ToUserName}</span>
                      </div>
                      {debt.Description && (
                        <div className="debt-description">{debt.Description}</div>
                      )}
                    </div>
                    <div className="debt-actions">
                      {debt.Status === 'pending' && (
                        <button 
                          className="mark-paid-button"
                          onClick={() => handleMarkPaid(debt.DebtID)}
                          title="Mark as paid"
                        >
                          ✓
                        </button>
                      )}
                      <button 
                        className="delete-debt-button"
                        onClick={() => handleDeleteDebt(debt.DebtID)}
                        title="Delete debt"
                      >
                        ×
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-state">
                <FaBalanceScale className="empty-state-icon" />
                <h3>No debts in this group yet</h3>
                <p>Add a group expense to get started!</p>
              </div>
            )}
          </div>
        </div>

        <div className="side-content">
          <div className="debt-relations-section">
            <h2>Total Debt Relations</h2>
            <div className="debt-relations-list">
              {debtRelations.map((relation, index) => (
                <div key={index} className="debt-relation-card">
                  <div className="relation-users">
                    <span className="debtor">{relation.fromUser}</span>
                    <span className="relation-arrow">owes</span>
                    <span className="creditor">{relation.toUser}</span>
                  </div>
                  <div className="relation-amount">
                    ${relation.totalAmount.toFixed(2)}
                  </div>
                  <div className="relation-actions">
                    <button 
                      className="mark-paid-button"
                      onClick={() => handleMarkPaid(relation.debtId)}
                      title="Mark as paid"
                    >
                      ✓
                    </button>
                    <button 
                      className="delete-debt-button"
                      onClick={() => handleDeleteDebt(relation.debtId)}
                      title="Delete debt"
                    >
                      ×
                    </button>
                  </div>
                </div>
              ))}
              {debtRelations.length === 0 && (
                <div className="no-relations">
                  No active debts between members
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {showAddDebtModal && (
        <div className="modal">
          <div className="modal-content">
            <h3>Add Group Expense</h3>
            <form onSubmit={handleAddExpense}>
              <div className="form-group">
                <label>Paid By</label>
                <select 
                  value={newExpense.paidByUserId}
                  onChange={(e) => setNewExpense({...newExpense, paidByUserId: e.target.value})}
                  required
                >
                  <option value="">Select who paid</option>
                  {members.map(member => (
                    <option key={member.UserID} value={member.UserID}>
                      {member.Name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Total Amount ($)</label>
                <input 
                  type="number"
                  step="0.01"
                  value={newExpense.amount}
                  onChange={(e) => setNewExpense({...newExpense, amount: e.target.value})}
                  required
                />
                {newExpense.amount && (
                  <div className="split-info">
                    Each person will pay: ${(parseFloat(newExpense.amount) / members.length).toFixed(2)}
                  </div>
                )}
              </div>

              <div className="form-group">
                <label>Description</label>
                <input 
                  type="text"
                  value={newExpense.description}
                  onChange={(e) => setNewExpense({...newExpense, description: e.target.value})}
                  placeholder="e.g., Dinner, Movie tickets, etc."
                  required
                />
              </div>

              <div className="modal-actions">
                <button type="button" onClick={() => setShowAddDebtModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="submit-button">
                  Add Expense
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <Dialog
        isOpen={showDeleteDialog}
        message="Are you sure you want to delete this debt?"
        onConfirm={confirmDeleteDebt}
        onCancel={() => setShowDeleteDialog(false)}
      />

      <Dialog
        isOpen={showDialog}
        message="Are you sure you want to delete this group?"
        onConfirm={handleConfirmDelete}
        onCancel={() => setShowDialog(false)}
      />

      <button className="delete-group-button" onClick={handleDeleteClick}>
        <FaTrash />
        Delete Group
      </button>

      {showDeleteModal && (
        <div className="delete-confirm-modal">
          <div className="delete-confirm-content">
            <h3>Delete Group</h3>
            <p>Are you sure you want to delete this group? This action cannot be undone.</p>
            <div className="delete-confirm-buttons">
              <button className="confirm-delete" onClick={handleConfirmDelete}>
                Delete
              </button>
              <button className="cancel-delete" onClick={() => setShowDeleteModal(false)}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GroupDetails;
