import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from routes.users import users

app = Flask(__name__)  

app.register_blueprint(users)

@app.route("/")
def home():
    return "FinanceTracker API is running!"

if __name__ == "__main__":
    app.run(debug=True)
