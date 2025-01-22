from flask import Blueprint, jsonify, request
from mysql.connector import Error
from ..database_config import get_db_connection

notifications = Blueprint('notifications', __name__)

@notifications.route('/notifications', methods=['GET'])
def get_notifications():
    user_id = request.args.get('userId')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT * FROM notifications 
            WHERE UserID = %s 
            ORDER BY CreatedDate DESC
        """, (user_id,))
        
        notifications = cursor.fetchall()
        return jsonify(notifications)

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@notifications.route('/notifications/mark-read', methods=['POST'])
def mark_notification_read():
    data = request.json
    notification_id = data.get('notificationId')
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("""
            UPDATE notifications 
            SET IsRead = TRUE 
            WHERE NotificationID = %s
        """, (notification_id,))
        
        connection.commit()
        return jsonify({'message': 'Notification marked as read'}), 200

    except Error as e:
        print(f"Mark read error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def create_debt_notification(user_id, from_user_name, amount, debt_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        title = "New Debt Added"
        message = f"{from_user_name} owes you ${amount}"
        
        cursor.execute("""
            INSERT INTO notifications 
            (UserID, Title, Message, Type, RelatedID) 
            VALUES (%s, %s, %s, 'debt', %s)
        """, (user_id, title, message, debt_id))
        
        connection.commit()

    except Error as e:
        print(f"Create notification error: {str(e)}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
