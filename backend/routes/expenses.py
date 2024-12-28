from flask import Blueprint, request, jsonify
from backend.database_config import get_db_connection

# Blueprint tanımı
expenses = Blueprint('expenses', __name__)

# Harcama ekleme endpoint'i
@expenses.route('/expenses', methods=['POST'])
def add_expense():
    # JSON isteğinden gelen verileri al
    data = request.json
    group_id = data.get('group_id')
    user_id = data.get('user_id')
    amount = data.get('amount')
    description = data.get('description')

    # Eksik veri kontrolü
    if not all([group_id, user_id, amount]):
        return jsonify({'error': 'Group ID, User ID, and amount are required!'}), 400

    # Veritabanı bağlantısı
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Harcamayı veritabanına ekle
        cursor.execute("""
            INSERT INTO Expenses (GroupID, UserID, Amount, Description, ExpenseDate)
            VALUES (:group_id, :user_id, :amount, :description, SYSDATE)
        """, {
            'group_id': group_id,
            'user_id': user_id,
            'amount': amount,
            'description': description
        })
        connection.commit()
    except Exception as e:
        # Hata durumunda işlemi geri al
        connection.rollback()
        return jsonify({'error': f'Failed to add expense: {str(e)}'}), 500
    finally:
        # Kaynakları temizle
        cursor.close()
        connection.close()

    return jsonify({'message': 'Expense added successfully!'}), 201

# Harcamaları listeleme endpoint'i
@expenses.route('/expenses', methods=['GET'])
def list_expenses():
    # Veritabanı bağlantısı
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Tüm harcamaları sorgula
        cursor.execute("SELECT ExpenseID, GroupID, UserID, Amount, Description, ExpenseDate FROM Expenses")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        
        # Exclude 'Date' field from the response if it exists
        result = [
            {key: value for key, value in zip(columns, row) if key != 'Date'} 
            for row in rows
        ]
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve expenses: {str(e)}'}), 500
    finally:
        # Kaynakları temizle
        cursor.close()
        connection.close()

    return jsonify(result), 200

# Belirli bir harcamayı görüntüleme endpoint'i
@expenses.route('/expenses/<int:expense_id>', methods=['GET'])
def get_expense(expense_id):
    # Veritabanı bağlantısı
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Belirtilen ID'ye göre harcamayı sorgula
        cursor.execute("SELECT ExpenseID, GroupID, UserID, Amount, Description, ExpenseDate FROM Expenses WHERE ExpenseID = :expense_id", {'expense_id': expense_id})
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Expense not found!'}), 404

        # Harcamayı JSON formatına dönüştür
        columns = [col[0] for col in cursor.description]
        result = {key: value for key, value in zip(columns, row) if key != 'Date'}
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve expense: {str(e)}'}), 500
    finally:
        # Kaynakları temizle
        cursor.close()
        connection.close()

    return jsonify(result), 200
