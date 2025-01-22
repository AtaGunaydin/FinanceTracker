import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='finance_tracker',
            user='saldo_user',
            password='Barbunya44!',
            port=3306
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        raise e