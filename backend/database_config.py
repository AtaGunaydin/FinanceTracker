import cx_Oracle

def get_db_connection():
    connection = cx_Oracle.connect(
        user="C##OZGUVEN",
        password="financetracker",
        dsn="localhost:1521/ORCLCDB"
    )
    return connection