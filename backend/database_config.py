import cx_Oracle

def get_db_connection():
    connection = cx_Oracle.connect(
        user="C##ISE304",
        password="financetracker",
        dsn="localhost:1521/ORCLCDB"
    )
    return connection