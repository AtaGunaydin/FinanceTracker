# Saldo - Expense Sharing App

## 🛠 Backend Setup

1. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # For Windows: .venv\Scripts\activate
   ```

2. **Install backend dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Setup MySQL Database:**

   ```bash
   mysql -u root -p
   ```

   - Enter your MySQL password when prompted.
   - Create the database:

     ```sql
     CREATE DATABASE finance_tracker;
     ```

   - Copy and paste the contents of `tables.sql` into the MySQL console.

4. **Create a `.env` file in the backend directory with:**

   ```plaintext
   DB_HOST=localhost
   DB_USER=your_mysql_username
   DB_PASSWORD=your_mysql_password
   DB_NAME=finance_tracker
   JWT_SECRET=your_secret_key
   ```

5. **Start the backend server:**

   ```bash
   python -m backend.app
   ```

## 🌐 Frontend Setup

1. **Navigate to the frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Start the frontend:**

   ```bash
   npm start
   ```

## 📝 Notes

- Ensure your backend server is running before starting the frontend or mobile app.
- Make sure your mobile device is on the same network as your development machine for the mobile app to connect to the backend.

This guide provides all the necessary steps to set up the project from scratch. If you encounter any issues, feel free to reach out for more detailed assistance.
