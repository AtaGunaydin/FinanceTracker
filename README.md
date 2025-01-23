 # Saldo - Smart Expense Management App

Welcome to the Saldo app! This guide will help you set up the project on your local machine.

## 🌟 Overview

Saldo is a cutting-edge expense management application designed to simplify the way you handle shared expenses. Whether you're managing household bills, planning a group trip, or splitting costs with roommates, Saldo makes it effortless and efficient. With its intuitive interface and robust features, Saldo ensures that you stay on top of your finances with ease.

### Why Saldo?

- **Effortless Expense Tracking**: Automatically split bills and track expenses in real-time.
- **Smart Notifications**: Stay informed with timely alerts about new expenses, payments, and reminders.
- **Secure and Reliable**: Built with top-notch security features to protect your data and ensure privacy.
- **User-Friendly Interface**: Designed with simplicity in mind, making it accessible for everyone.

## 📦 Repository

Clone the repository to your local machine:


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
