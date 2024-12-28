from flask import Blueprint, request, jsonify
from backend.database_config import get_db_connection

notifications = Blueprint('notifications', __name__)

# Yeni bir bildirim ekleme endpoint'i
@notifications.route('/notifications', methods=['POST'])
def add_notification():
    data = request.json
    user_id = data.get('user_id')
    message = data.get('message')

    if not all([user_id, message]):
        return jsonify({'error': 'User ID and message are required!'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO Notifications (UserID, Message, ReadStatus)
            VALUES (:user_id, :message, 0)
        """, {
            'user_id': user_id,
            'message': message
        })
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({'error': f'Failed to add notification: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'Notification added successfully!'}), 201

# Tüm bildirimleri listeleme endpoint'i
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

# Belirli bir bildirimi görüntüleme endpoint'i
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

# Belirli bir bildirimi "okundu" olarak işaretleme endpoint'i
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
