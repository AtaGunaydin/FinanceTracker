import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from flask import Flask
from routes.users import users
from routes.groups import groups
from routes.expenses import expenses
from routes.notifications import notifications
from routes.debts import debts


app = Flask(__name__)

# Blueprintleri kaydet
app.register_blueprint(users)
app.register_blueprint(groups)
app.register_blueprint(expenses)
app.register_blueprint(notifications)
app.register_blueprint(debts)



@app.route("/")
def home():
    return "FinanceTracker API is running!"

if __name__ == "__main__":
    app.run(debug=True)


@app.route("/health")
def health_check():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM DUAL")
        cursor.close()
        connection.close()
        return "Database connection is healthy!", 200
    except Exception as e:
        return f"Database connection failed: {str(e)}", 500