import sqlite3

def create_connection():
    # Connect to the currency exchange database
    conn = sqlite3.connect("money_exchange.db")
    # Enable foreign key constraint support
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    
    # 1. Branch Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Branch (
            BranchID INTEGER PRIMARY KEY AUTOINCREMENT,
            BranchName TEXT NOT NULL,
            Status TEXT NOT NULL,
            City TEXT NOT NULL,
            Location TEXT NOT NULL
        )
    ''')
    
    # 2. Customer Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
            Customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Customer_name TEXT NOT NULL,
            Email TEXT UNIQUE NOT NULL,
            Address TEXT,
            Phone_number TEXT
        )
    ''')
    
    # 3. Account Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Account (
            Account_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Customer_id INTEGER,
            BranchID INTEGER,
            Balance DECIMAL(18, 4) NOT NULL DEFAULT 0.0000,
            Account_type TEXT NOT NULL,
            FOREIGN KEY (Customer_id) REFERENCES Customer(Customer_id) ON DELETE CASCADE,
            FOREIGN KEY (BranchID) REFERENCES Branch(BranchID) ON DELETE SET NULL
        )
    ''')
    
    # 4. Transaction Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "Transaction" (
            Transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Account_ID INTEGER,
            Customer_ID INTEGER,
            Trans_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            Trans_type TEXT NOT NULL,
            FOREIGN KEY (Account_ID) REFERENCES Account(Account_ID) ON DELETE CASCADE,
            FOREIGN KEY (Customer_ID) REFERENCES Customer(Customer_id) ON DELETE CASCADE
        )
    ''')
    
    # 5. Exchange Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Exchange (
            Exchange_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Transaction_ID INTEGER UNIQUE,
            Account_ID INTEGER,
            Exchange_rate DECIMAL(18, 4) NOT NULL,
            Date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (Transaction_ID) REFERENCES "Transaction"(Transaction_id) ON DELETE CASCADE,
            FOREIGN KEY (Account_ID) REFERENCES Account(Account_ID) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()