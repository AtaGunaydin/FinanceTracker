from flask import Blueprint, request, jsonify
from ..database_config import get_db_connection
from mysql.connector import Error

debts = Blueprint('debts', __name__)

@debts.route('/groups/<int:group_id>/debts', methods=['POST'])
def create_debt(group_id):
    data = request.json
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        print(f"Creating debt with data: {data}")  # Debug log

        # Borç oluştur
        cursor.execute("""
            INSERT INTO debts (GroupID, FromUserID, ToUserID, Amount, Description, Status)
            VALUES (%s, %s, %s, %s, %s, 'pending')
        """, (group_id, data['fromUserId'], data['toUserId'], data['amount'], data['description']))
        
        debt_id = cursor.lastrowid
        print(f"Created debt with ID: {debt_id}")  # Debug log

        # Borç alan kişinin adını al
        cursor.execute("SELECT Name FROM users WHERE UserID = %s", (data['fromUserId'],))
        from_user = cursor.fetchone()
        from_user_name = from_user[0] if from_user else 'Someone'
        print(f"From user name: {from_user_name}")  # Debug log

        # Notifikasyon oluştur
        notification_data = (
            data['toUserId'],
            'New Debt Added',
            f"{from_user_name} owes you ${data['amount']}",
            debt_id
        )
        print(f"Creating notification with data: {notification_data}")  # Debug log

        cursor.execute("""
            INSERT INTO notifications (UserID, Title, Message, Type, RelatedID, IsRead, CreatedDate)
            VALUES (%s, %s, %s, 'debt', %s, FALSE, NOW())
        """, notification_data)

        connection.commit()
        print("Transaction committed successfully")  # Debug log
        return jsonify({'message': 'Debt created successfully'}), 201

    except Error as e:
        print(f"Error creating debt: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@debts.route('/debts', methods=['GET'])
def list_debts():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM debts")
        debts = cursor.fetchall()
        return jsonify(debts), 200
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@debts.route('/debts/<int:debt_id>', methods=['GET'])
def get_debt(debt_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM Debts WHERE DebtID = :debt_id", {'debt_id': debt_id})
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Debt not found!'}), 404

        columns = [col[0] for col in cursor.description]
        result = dict(zip(columns, row))
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve debt: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(result), 200

@debts.route('/debts/<int:debt_id>', methods=['PUT'])
def update_debt_status(debt_id):
    data = request.json
    status = data.get('status')

    if not status:
        return jsonify({'error': 'Status is required!'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE Debts
            SET Status = :status
            WHERE DebtID = :debt_id
        """, {'status': status, 'debt_id': debt_id})
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'Debt not found!'}), 404
    except Exception as e:
        connection.rollback()
        return jsonify({'error': f'Failed to update debt: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'Debt status updated successfully!'}), 200

@debts.route('/debts/<int:debt_id>', methods=['DELETE'])
def delete_debt(debt_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM Debts
            WHERE DebtID = :debt_id
        """, {'debt_id': debt_id})
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'Debt not found!'}), 404
    except Exception as e:
        connection.rollback()
        return jsonify({'error': f'Failed to delete debt: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'Debt deleted successfully!'}), 200
