CREATE TABLE users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Phone VARCHAR(15),
    Password VARCHAR(255) NOT NULL,
    Currency VARCHAR(3)
);

CREATE TABLE notifications (
    NotificationID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Title VARCHAR(100) NOT NULL,
    Message TEXT NOT NULL,
    Type VARCHAR(20) NOT NULL,
    IsRead TINYINT(1) DEFAULT 0,
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    RelatedID INT,
    FOREIGN KEY (UserID) REFERENCES users(UserID)
);

CREATE TABLE groupsaldo (
    GroupID INT AUTO_INCREMENT PRIMARY KEY,
    GroupName VARCHAR(100) NOT NULL,
    CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE groupmembers (
    GroupID INT NOT NULL,
    UserID INT NOT NULL,
    PRIMARY KEY (GroupID, UserID),
    FOREIGN KEY (GroupID) REFERENCES groupsaldo(GroupID),
    FOREIGN KEY (UserID) REFERENCES users(UserID)
);

CREATE TABLE expenses (
    ExpenseID INT AUTO_INCREMENT PRIMARY KEY,
    GroupID INT NOT NULL,
    UserID INT NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    Description VARCHAR(255) NOT NULL,
    Date DATE NOT NULL,
    FOREIGN KEY (GroupID) REFERENCES groupsaldo(GroupID),
    FOREIGN KEY (UserID) REFERENCES users(UserID)
);

CREATE TABLE debts (
    DebtID INT AUTO_INCREMENT PRIMARY KEY,
    FromUserID INT NOT NULL,
    ToUserID INT NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    Status VARCHAR(20) NOT NULL,
    GroupID INT NOT NULL,
    Description TEXT,
    FOREIGN KEY (FromUserID) REFERENCES users(UserID),
    FOREIGN KEY (ToUserID) REFERENCES users(UserID),
    FOREIGN KEY (GroupID) REFERENCES groupsaldo(GroupID)
);

CREATE INDEX idx_user_email ON users(Email);
CREATE INDEX idx_notifications_user ON notifications(UserID, IsRead);
CREATE INDEX idx_expense_date ON expenses(Date);
CREATE INDEX idx_debt_status ON debts(Status);

SHOW TABLES;



