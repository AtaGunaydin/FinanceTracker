import sys
import os
from flask import Blueprint, request, jsonify
from backend.database_config import get_db_connection

users = Blueprint('users', __name__)

# Endpoint: Adding User 
@users.route('/users', methods=['POST'])
def add_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    currency = data.get('currency', 'USD')

    if not all([name, email, password]):
        return jsonify({'error': 'Name, email, and password are required!'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO Users (Name, Email, Phone, Password, Currency)
            VALUES (:name, :email, :phone, :password, :currency)
        """, {
            'name': name,
            'email': email,
            'phone': phone,
            'password': password,
            'currency': currency
        })
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({'error': f'Failed to add user: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'User added successfully!'}), 201

# Endpoint: Listing users
@users.route('/users', methods=['GET'])
def get_users():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM Users")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve users: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(result), 200

# Endpoint: Listing a specific user
@users.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM Users WHERE UserID = :user_id", {'user_id': user_id})
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'User not found!'}), 404

        columns = [col[0] for col in cursor.description]
        result = dict(zip(columns, row))
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve user: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(result), 200

# Endpoint: Updating password
@users.route('/users/<int:user_id>/password', methods=['PUT'])
def update_password(user_id):
    data = request.json
    new_password = data.get('password')

    if not new_password:
        return jsonify({'error': 'Password is required!'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE Users SET Password = :password WHERE UserID = :user_id", {
            'password': new_password,
            'user_id': user_id
        })
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'User not found!'}), 404
    except Exception as e:
        connection.rollback()
        return jsonify({'error': f'Failed to update password: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'Password updated successfully!'}), 200

# Endpoint: Searching user
@users.route('/users/search', methods=['GET'])
def search_users():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Query parameter is required!'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT * FROM Users
            WHERE LOWER(Name) LIKE LOWER(:query) OR LOWER(Email) LIKE LOWER(:query)
        """, {'query': f'%{query}%'});
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return jsonify({'error': f'Failed to search users: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(result), 200

# Endpoint: Deleting a User
@users.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM Users WHERE UserID = :user_id", {'user_id': user_id})
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'User not found!'}), 404
    except Exception as e:
        connection.rollback()
        return jsonify({'error': f'Failed to delete user: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'User deleted successfully!'}), 200
