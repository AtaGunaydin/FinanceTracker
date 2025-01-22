from flask import Blueprint, jsonify, request
from ..database_config import get_db_connection
from mysql.connector import Error

stats = Blueprint('stats', __name__)

@stats.route('/stats', methods=['GET'])
def get_stats():
    user_id = request.headers.get('User-ID')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT COUNT(DISTINCT g.GroupID) as totalGroups
            FROM groupsaldo g
            JOIN groupmembers gm ON g.GroupID = gm.GroupID
            WHERE gm.UserID = %s
        """, (user_id,))
        total_groups = cursor.fetchone()['totalGroups']

        cursor.execute("""
            SELECT 
                COUNT(*) as totalDebts,
                SUM(CASE WHEN Status = 'pending' THEN 1 ELSE 0 END) as activeDebts,
                SUM(Amount) as totalAmount
            FROM debts
            WHERE FromUserID = %s OR ToUserID = %s
        """, (user_id, user_id))
        debt_stats = cursor.fetchone()

        return jsonify({
            'totalGroups': total_groups,
            'totalDebts': debt_stats['totalDebts'] or 0,
            'activeDebts': debt_stats['activeDebts'] or 0,
            'totalAmount': float(debt_stats['totalAmount'] or 0)
        }), 200

    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close() 