from flask import Blueprint, request, jsonify
from backend.database_config import get_db_connection
import cx_Oracle  # Import cx_Oracle

notifications = Blueprint('notifications', __name__)

# Endpoint to add a new notification
@notifications.route('/notifications', methods=['POST'])
def add_notification():
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')

    if not user_id or not message:
        return jsonify({'error': 'User ID and message are required!'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        notification_id = cursor.var(cx_Oracle.NUMBER)

        cursor.execute("""
            INSERT INTO Notifications (UserID, Message, ReadStatus)
            VALUES (:user_id, :message, 0)
            RETURNING NotificationID INTO :notification_id
        """, {
            'user_id': user_id,
            'message': message,
            'notification_id': notification_id
        })

        connection.commit()

        new_notification_id = int(notification_id.getvalue()[0])

    except Exception as e:
        connection.rollback()
        print(f"Error during notification creation: {e}")
        return jsonify({'error': f'Failed to create notification: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'Notification created successfully!', 'notification_id': new_notification_id}), 201

# Endpoint to list all notifications
@notifications.route('/notifications', methods=['GET'])
def list_notifications():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM Notifications")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve notifications: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(result), 200

# Endpoint to retrieve a specific notification
@notifications.route('/notifications/<int:notification_id>', methods=['GET'])
def get_notification(notification_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM Notifications WHERE NotificationID = :notification_id", {'notification_id': notification_id})
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Notification not found!'}), 404

        columns = [col[0] for col in cursor.description]
        result = dict(zip(columns, row))
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve notification: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(result), 200

# Endpoint to mark a notification as read
@notifications.route('/notifications/<int:notification_id>', methods=['PUT'])
def mark_notification_as_read(notification_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE Notifications
            SET ReadStatus = 1
            WHERE NotificationID = :notification_id
        """, {'notification_id': notification_id})
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'Notification not found!'}), 404
    except Exception as e:
        connection.rollback()
        return jsonify({'error': f'Failed to update notification: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'Notification marked as read!'}), 200
