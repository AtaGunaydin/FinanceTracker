from flask import Blueprint, request, jsonify
from backend.database_config import get_db_connection

debts = Blueprint('debts', __name__)

# POST /debts: Yeni bir borç ekleme
@debts.route('/debts', methods=['POST'])
def add_debt():
    data = request.json
    from_user_id = data.get('from_user_id')
    to_user_id = data.get('to_user_id')
    amount = data.get('amount')

    if not all([from_user_id, to_user_id, amount]):
        return jsonify({'error': 'FromUserID, ToUserID, and amount are required!'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO Debts (FromUserID, ToUserID, Amount, Status)
            VALUES (:from_user_id, :to_user_id, :amount, 'Pending')
        """, {
            'from_user_id': from_user_id,
            'to_user_id': to_user_id,
            'amount': amount
        })
        connection.commit()
    except Exception as e:
        connection.rollback()
        return jsonify({'error': f'Failed to add debt: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'Debt added successfully!'}), 201

# GET /debts: Tüm borçları listeleme
@debts.route('/debts', methods=['GET'])
def list_debts():
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM Debts")
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve debts: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify(result), 200

# GET /debts/<debt_id>: Belirli bir borcu görüntüleme
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

# PUT /debts/<debt_id>: Borç durumunu güncelleme
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
        # Borcu sil
        cursor.execute("""
            DELETE FROM Debts
            WHERE DebtID = :debt_id
        """, {'debt_id': debt_id})
        connection.commit()

        # Eğer borç bulunamadıysa
        if cursor.rowcount == 0:
            return jsonify({'error': 'Debt not found!'}), 404
    except Exception as e:
        connection.rollback()
        return jsonify({'error': f'Failed to delete debt: {str(e)}'}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'message': 'Debt deleted successfully!'}), 200
