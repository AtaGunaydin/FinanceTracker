import sys
import os
from flask import Blueprint, request, jsonify, make_response
from backend.database_config import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import Error
from ..utils.auth import generate_token, token_required
from ..utils.password_validator import validate_password

users = Blueprint('users', __name__)

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
        hashed_password = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO Users (Name, Email, Phone, Password, Currency)
            VALUES (:name, :email, :phone, :password, :currency)
        """, {
            'name': name,
            'email': email,
            'phone': phone,
            'password': hashed_password,
            'currency': currency
        })
        connection.commit()
    except Exception as e:
        print(f"Error during user creation: {e}")
        connection.rollback()
        return jsonify({'error': f'Failed to add user: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'User added successfully!'}), 201

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
        print(f"Error retrieving users: {e}")
        return jsonify({'error': f'Failed to retrieve users: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(result), 200

@users.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user_id, user_id):
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT UserID, Name, Email 
            FROM users 
            WHERE UserID = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        
        if user:
            return jsonify(user), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@users.route('/users/<int:user_id>/password', methods=['PUT'])
def update_password(user_id):
    try:
        data = request.get_json()
        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')

        if not current_password or not new_password:
            return jsonify({'error': 'Missing required fields'}), 400

        password_errors = validate_password(new_password)
        if password_errors:
            return jsonify({'error': password_errors[0]}), 400

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT Password 
            FROM users 
            WHERE UserID = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        if not check_password_hash(user['Password'], current_password):
            return jsonify({'error': 'Current password is incorrect'}), 400

        hashed_password = generate_password_hash(new_password)
        cursor.execute("""
            UPDATE users 
            SET Password = %s 
            WHERE UserID = %s
        """, (hashed_password, user_id))
        
        connection.commit()
        
        return jsonify({'message': 'Password updated successfully'}), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@users.route('/users/search', methods=['GET'])
def search_users():
    term = request.args.get('term', '')
    current_user_id = request.headers.get('User-ID')
    
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401
        
    if len(term) < 2:
        return jsonify([]), 200

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT UserID, Name, Email 
            FROM Users 
            WHERE (Name LIKE %s OR Email LIKE %s)
            AND UserID != %s
            LIMIT 10
        """, (f'%{term}%', f'%{term}%', current_user_id))
        
        users = cursor.fetchall()
        return jsonify(users), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

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
        print(f"Error deleting user: {e}")
        return jsonify({'error': f'Failed to delete user: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'User deleted successfully!'}), 200

@users.route('/users/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')

        if not all([name, email, password, phone]):
            return jsonify({'error': 'All fields are required'}), 400

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE Email = %s", (email,))
        if cursor.fetchone():
            return jsonify({'error': 'Email already registered'}), 400

        hashed_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO users (Name, Email, Password, Phone, Currency)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, hashed_password, phone, 'USD'))  

        connection.commit()
        return jsonify({'message': 'Registration successful'}), 201

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@users.route('/users/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT UserID, Name, Email, Password 
            FROM users 
            WHERE Email = %s
        """, (email,))

        user = cursor.fetchone()

        if user and check_password_hash(user['Password'], password):
            token = generate_token(user['UserID'])
            return jsonify({
                'token': token,
                'user_id': user['UserID'],
                'name': user['Name']
            }), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@users.route('/users/profile', methods=['GET'])
def get_user_profile():
    user_id = request.headers.get('User-ID')
    print(f"Debug - User ID from header: {user_id}")
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = """
            SELECT Name, Email 
            FROM Users 
            WHERE UserID = %s
        """
        
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        
        print(f"Debug - Query result: {user}")
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        result = {
            'name': user['Name'],
            'email': user['Email']
        }
        
        return jsonify(result), 200
        
    except Error as e:
        print(f"Debug - Database error: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@users.route('/users/profile/password', methods=['PUT'])
def change_password():
    user_id = request.headers.get('User-ID')
    data = request.json
    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')
    
    if not all([user_id, current_password, new_password]):
        return jsonify({'error': 'All fields are required'}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT Password 
            FROM Users 
            WHERE UserID = %s
        """, (user_id,))
        
        user = cursor.fetchone()
        
        if not user or not check_password_hash(user['Password'], current_password):
            return jsonify({'error': 'Current password is incorrect'}), 401
            
        hashed_password = generate_password_hash(new_password)
        cursor.execute("""
            UPDATE Users 
            SET Password = %s 
            WHERE UserID = %s
        """, (hashed_password, user_id))
        
        connection.commit()
        return jsonify({'message': 'Password updated successfully'}), 200
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
