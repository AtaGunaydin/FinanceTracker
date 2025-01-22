from flask import Blueprint, request, jsonify
from ..database_config import get_db_connection
from mysql.connector import Error
from datetime import datetime

groups = Blueprint('groups', __name__)

@groups.route('/groups', methods=['POST'])
def create_group():
    data = request.json
    group_name = data.get('GroupName')
    members = data.get('Members', [])
    creator_id = request.headers.get('User-ID')

    if not group_name:
        return jsonify({'error': 'Group name is required!'}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            INSERT INTO groupsaldo (GroupName, CreatedDate)
            VALUES (%s, NOW())
        """, (group_name,))
        
        group_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO groupmembers (GroupID, UserID)
            VALUES (%s, %s)
        """, (group_id, creator_id))

        for member_id in members:
            cursor.execute("""
                INSERT INTO groupmembers (GroupID, UserID)
                VALUES (%s, %s)
            """, (group_id, member_id))
        
        connection.commit()
        return jsonify({
            'message': 'Group created successfully',
            'group_id': group_id
        }), 201

    except Error as e:
        if 'connection' in locals():
            connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@groups.route('/groups', methods=['GET'])
def get_user_groups():
    user_id = request.headers.get('User-ID')
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT g.* 
            FROM groupsaldo g
            JOIN groupmembers gm ON g.GroupID = gm.GroupID
            WHERE gm.UserID = %s
            ORDER BY g.CreatedDate DESC
        """, (user_id,))
        
        groups = cursor.fetchall()
        return jsonify(groups), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@groups.route('/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM debts 
            WHERE GroupID = %s
        """, (group_id,))

        cursor.execute("""
            DELETE FROM groupmembers 
            WHERE GroupID = %s
        """, (group_id,))

        cursor.execute("""
            DELETE FROM groupsaldo 
            WHERE GroupID = %s
        """, (group_id,))

        connection.commit()
        return jsonify({'message': 'Group deleted successfully'}), 200

    except Error as e:
        if 'connection' in locals():
            connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@groups.route('/groups/<int:group_id>', methods=['GET'])
def get_group_details(group_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM groupsaldo 
            WHERE GroupID = %s
        """, (group_id,))
        
        group = cursor.fetchone()
        
        if not group:
            return jsonify({'error': 'Group not found'}), 404

        return jsonify(group), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@groups.route('/groups/<int:group_id>/members', methods=['GET'])
def get_group_members(group_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT u.UserID, u.Name, u.Email
            FROM Users u
            JOIN groupmembers gm ON u.UserID = gm.UserID
            WHERE gm.GroupID = %s
        """, (group_id,))
        
        members = cursor.fetchall()
        return jsonify(members), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@groups.route('/groups/<int:group_id>/debts', methods=['GET'])
def get_group_debts(group_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT 
                debts.DebtID,
                debts.FromUserID,
                debts.ToUserID,
                debts.Amount,
                debts.Status,
                debts.GroupID,
                u1.Name as FromUserName,
                u2.Name as ToUserName
            FROM debts
            JOIN Users u1 ON debts.FromUserID = u1.UserID
            JOIN Users u2 ON debts.ToUserID = u2.UserID
            WHERE debts.GroupID = %s
            ORDER BY debts.DebtID DESC
        """, (group_id,))
        
        debts = cursor.fetchall()
        
        for debt in debts:
            if debt.get('Amount'):
                debt['Amount'] = float(debt['Amount'])
            
        return jsonify(debts), 200

    except Error as e:
        print(f"Database error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@groups.route('/groups/<int:group_id>/debts', methods=['POST'])
def add_group_debt(group_id):
    data = request.json
    from_user_id = data.get('fromUserId')
    to_user_id = data.get('toUserId')
    amount = data.get('amount')
    description = data.get('description', '')
    status = data.get('status', 'pending')

    if not all([from_user_id, to_user_id, amount]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM groupmembers 
            WHERE GroupID = %s AND UserID IN (%s, %s)
        """, (group_id, from_user_id, to_user_id))
        
        if cursor.fetchone()['count'] != 2:
            return jsonify({'error': 'Users must be members of the group'}), 400

        cursor.execute("""
            INSERT INTO debts 
            (FromUserID, ToUserID, Amount, Description, Status, GroupID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (from_user_id, to_user_id, amount, description, status, group_id))
        
        debt_id = cursor.lastrowid

        cursor.execute("""
            SELECT Name FROM users WHERE UserID = %s
        """, (from_user_id,))
        from_user = cursor.fetchone()
        from_user_name = from_user['Name'] if from_user else 'Someone'

        cursor.execute("""
            INSERT INTO notifications 
            (UserID, Title, Message, Type, RelatedID) 
            VALUES (%s, %s, %s, 'debt', %s)
        """, (
            to_user_id,
            "New Debt Added",
            f"{from_user_name} owes you ${amount}",
            debt_id
        ))
        
        connection.commit()
        return jsonify({'message': 'Debt added successfully', 'debtId': debt_id}), 201

    except Error as e:
        print(f"Error adding debt: {str(e)}")
        if 'connection' in locals():
            connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@groups.route('/groups/<int:group_id>/debts/<int:debt_id>', methods=['DELETE'])
def delete_debt(group_id, debt_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            DELETE FROM debts 
            WHERE DebtID = %s
        """, (debt_id,))
        
        connection.commit()
        return jsonify({'message': 'Debt deleted successfully'}), 200

    except Error as e:
        if 'connection' in locals():
            connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@groups.route('/groups/<int:group_id>/debts/<int:debt_id>/mark-paid', methods=['PUT'])
def mark_debt_paid(group_id, debt_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            UPDATE debts 
            SET Status = 'paid' 
            WHERE DebtID = %s AND GroupID = %s
        """, (debt_id, group_id))
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Debt not found'}), 404
            
        connection.commit()
        
        cursor.execute("""
            SELECT d.*, u1.Name as FromUserName, u2.Name as ToUserName
            FROM debts d
            JOIN users u1 ON d.FromUserID = u1.UserID
            JOIN users u2 ON d.ToUserID = u2.UserID
            WHERE d.DebtID = %s
        """, (debt_id,))
        
        debt = cursor.fetchone()
        
        cursor.execute("""
            INSERT INTO notifications 
            (UserID, Title, Message, Type, RelatedID)
            VALUES (%s, %s, %s, 'payment', %s)
        """, (
            debt['ToUserID'],
            "Debt Paid",
            f"{debt['FromUserName']} paid their debt of ${debt['Amount']}",
            debt_id
        ))
        
        connection.commit()
        return jsonify({'message': 'Debt marked as paid'}), 200

    except Error as e:
        if 'connection' in locals():
            connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
