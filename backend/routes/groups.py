from flask import Blueprint, request, jsonify
from backend.database_config import get_db_connection

groups = Blueprint('groups', __name__)

# Endpoint to create a group
@groups.route('/groups', methods=['POST'])
def create_group():
    data = request.json
    group_name = data.get('GroupName')  

    if not group_name:
        return jsonify({'error': 'Group name is required!'}), 400

    if len(group_name) > 255:
        return jsonify({'error': 'Group name must not exceed 255 characters!'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM Groups WHERE GroupName = :group_name", {'group_name': group_name})
        count = cursor.fetchone()[0]
        if count > 0:
            return jsonify({'error': 'Group with this name already exists!'}), 400

        # Yeni grup ekle
        cursor.execute("""
            INSERT INTO Groups (GroupName, CreatedDate)
            VALUES (:group_name, SYSDATE)
        """, {'group_name': group_name})
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error during group creation: {e}")
        return jsonify({'error': f'Failed to create group: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'Group created successfully!'}), 201

# Endpoint to list all groups
@groups.route('/groups', methods=['GET'])
def list_groups():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM Groups")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve groups: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(result), 200

# Endpoint to add a user to a group
@groups.route('/groups/<int:group_id>/users', methods=['POST'])
def add_user_to_group(group_id):
    data = request.json
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'User ID is required!'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO GroupMembers (GroupID, UserID)
            VALUES (:group_id, :user_id)
        """, {'group_id': group_id, 'user_id': user_id})
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({'error': f'Failed to add user to group: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'User added to group successfully!'}), 201

