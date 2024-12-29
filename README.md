# FinanceTracker

FinanceTracker is a collaborative expense tracking application designed to help groups manage their shared expenses efficiently. It simplifies expense management, fosters accountability, and keeps everyone in the group informed about their financial contributions.

## Why FinanceTracker?
Managing shared expenses during group activities like vacations, projects, or events can be chaotic. FinanceTracker aims to solve this problem by offering an organized platform to track expenses, manage debts, and notify users of their financial status. It promotes transparency and ensures no one is left in the dark about group finances.

## How to Run the Application

### Prerequisites
- Python 3.8 or later
- Oracle Database
- Git

### Steps to Get Started
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/<your-username>/FinanceTracker.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd FinanceTracker
   ```
3. **Set Up a Virtual Environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate # On Windows, use `.venv\Scripts\activate`
   ```
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Configure the Database**:
   - Use the provided SQL scripts to create necessary tables and sequences in your Oracle Database.
   - Update `database_config.py` with your database credentials.
6. **Run the Application**:
   ```bash
   python backend/app.py
   ```
7. **Test the Application**:
   - Use Postman or any REST client to interact with the API endpoints.

Enjoy a hassle-free way to manage shared expenses!
