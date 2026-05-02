import sqlite3
from database import create_connection

# --- Customer Operations ---

def add_customer(name, email, address, phone):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO Customer (Customer_name, Email, Address, Phone_number) 
            VALUES (?, ?, ?, ?)
        ''', (name, email, address, phone))
        conn.commit()
        print("✅ Customer added successfully.")
    except sqlite3.IntegrityError:
        print("❌ Error: Email must be unique.")
    finally:
        conn.close()

def view_customers():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Customer")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_customer(customer_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Customer WHERE Customer_id = ?", (customer_id,))
    conn.commit()
    conn.close()
    print("🗑️ Customer deleted.")

# --- Branch Operations ---

def add_branch(name, status, city, location):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Branch (BranchName, Status, City, Location) 
        VALUES (?, ?, ?, ?)
    ''', (name, status, city, location))
    conn.commit()
    conn.close()
    print("✅ Branch added successfully.")

def view_branches():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Branch")
    rows = cursor.fetchall()
    conn.close()
    return rows