# Money Exchange Management System - Database Design

This project outlines a comprehensive database schema for a financial money exchange application. The design focuses on managing branch operations, customer accounts, and real-time currency exchange transactions.

---

## 1. Project Overview
The system is built to handle the complexities of multi-currency financial services, ensuring that every transaction is tracked from the specific branch down to the individual customer account and the applied exchange rate.

## 2. Entity-Relationship (ER) Components
The database consists of five core entities, each containing at least five attributes to maintain data integrity:

### **Branch**
Represents the physical office locations providing services.
* **BranchID (PK)**: Unique identifier for each branch.
* **BranchName**: The formal name of the branch.
* **Status**: Indicates if the branch is currently active or inactive.
* **City**: The city where the branch is located.
* **Location**: The specific address or coordinates of the branch.

### **Customer**
Stores the personal profile of the service users.
* **Customer_id (PK)**: Unique identifier for each client.
* **Customer_name**: Full name of the user.
* **Email**: Contact email for notifications.
* **Address**: Physical residence of the customer.
* **Phone_number**: Primary contact number.

### **Account**
Manages the funds and balances for customers at specific branches.
* **Account_ID (PK)**: Unique identifier for the account.
* **Customer_id (FK)**: References the account owner.
* **Balance**: Current amount of funds available.
* **Account_type**: The category of account (e.g., Savings, USD Wallet).

### **Transaction**
Logs every movement of funds within the system.
* **Transaction_id (PK)**: Unique transaction reference number.
* **Account_ID (FK)**: The account involved in the transaction.
* **Customer_ID (FK)**: The customer performing the transaction.
* **Trans_date**: Timestamp of the activity.
* **Trans_type**: Nature of the transaction (Deposit, Withdrawal, Exchange).

### **Exchange**
Captures the specific details of currency conversion events.
* **Exchange_ID (PK)**: Unique ID for the exchange record.
* **Transaction_ID (FK)**: Links to the parent transaction record.
* **Account_ID (FK)**: The specific account used for the exchange.
* **Exchange_rate**: The conversion rate applied at that moment.
* **Date**: The date of the exchange.

---

## 3. Relationship Logic
* **Branch to Account (1:N)**: A single branch can host multiple accounts, but an account is tied to one branch.
* **Customer to Account (1:N)**: A customer may open multiple accounts for different currencies.
* **Customer to Transaction (1:N)**: One customer can perform many transactions over time.
* **Account to Transaction (M:N)**: Multiple accounts can be involved in various transaction logs.
* **Transaction to Exchange (1:1)**: Every exchange record is uniquely associated with one specific transaction.

---

## 4. Technical Recommendations
1.  **Data Types**: Use `DECIMAL(18, 4)` for `Balance` and `Exchange_rate` to prevent rounding errors common with floating-point numbers.
2.  **Indexing**: Create indexes on Foreign Keys (`Customer_id`, `Account_ID`) to optimize query performance during high-volume transaction periods.
3.  **Audit Trail**: Ensure `Trans_date` and `Date` capture both date and time for precise auditing.