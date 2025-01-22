from flask import Blueprint, request, jsonify
from ..database_config import get_db_connection
from mysql.connector import Error

expenses = Blueprint('expenses', __name__)

@expenses.route('/expenses', methods=['POST'])
def add_expense():
    data = request.json
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            INSERT INTO expenses (GroupID, UserID, Amount, Description, Date)
            VALUES (%s, %s, %s, %s, NOW())
        """, (data['group_id'], data['user_id'], data['amount'], data['description']))
        
        connection.commit()
        return jsonify({'message': 'Expense added successfully'}), 201
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

@expenses.route('/expenses/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT ExpenseID, GroupID, UserID, Amount, Description, ExpenseDate FROM Expenses WHERE ExpenseID = :expense_id", {'expense_id': expense_id})
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Expense not found!'}), 404

        columns = [col[0] for col in cursor.description]
        result = {key: value for key, value in zip(columns, row) if key != 'Date'}
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve expense: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(result), 200


@expenses.route('/', methods=['GET'])
def list_expenses():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM Expenses")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve expenses: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(result), 200
