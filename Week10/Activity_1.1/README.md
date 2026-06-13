# User Management CLI

A lightweight **command-line** user account management system built entirely with Python's standard library.  
No `pip install` required — just `python main.py`.

---

## Table of Contents

- [Features Overview](#features-overview)
- [Function Call Flowchart](#function-call-flowchart)
- [Project Structure](#project-structure)
- [Module-by-Module Breakdown](#module-by-module-breakdown)
- [How to Run](#how-to-run)
- [Detailed Walkthrough](#detailed-walkthrough)
- [Expected Outputs](#expected-outputs)
- [Architecture & Design Principles](#architecture--design-principles)
- [Security Features](#security-features)
- [Requirements](#requirements)

---

## Features Overview

| # | Feature | User Story |
|---|---------|------------|
| 1 | **Register** | As a new user, I can create an account by providing my Full Name, Date of Birth, Email, Password, and a security question/answer so that I can access the system. |
| 2 | **Login** | As a registered user, I can log in with my Email and Password so that I can view my profile. |
| 3 | **Forgot Password** | As a user who forgot my password, I can answer my security question to reset it without needing admin help. |
| 4 | **List Users** | As an administrator (or for debugging), I can view all registered accounts. |
| 5 | **Exit** | As a user, I can exit the program cleanly. |

**Bonus built-in features:**
- Password is **masked on screen** during input (uses `getpass`).
- Password is **hashed with SHA-256** before storage (uses `hashlib`).
- Email format validation, password strength check, date validation.
- `Ctrl+C` at any prompt exits the program gracefully (no ugly traceback).
- Duplicate email detection prevents multiple registrations with the same email.

---

## Function Call Flowchart

This diagram shows how functions call each other when the program runs.  
An arrow `A → B` means "function A calls function B".

![Function Call Tree](design.svg)

**Colour legend:**
- 🟦 **Blue** — `main.py` (UI layer)  
- 🟩 **Green** — `auth.py` (business logic)  
- 🟧 **Orange** — `database.py` (persistence)  
- 🟪 **Purple** — `utils.py` (validation)  
- 🟥 **Red** — `models.py` (data model)  
- ⬜ **Grey** — `data/users.db` (SQLite)  
- ─ ─ Dashed arrows = reads/writes to the database

---

## Project Structure

```
Activity_1.1/
├── main.py          # CLI entry point — menus, prompts, screen functions
├── auth.py          # Business logic — register, login, forgot/reset password
├── database.py      # Persistence — SQLite CRUD operations
├── utils.py         # Utilities — password hashing, input validation, formatting
├── models.py        # Data model — User dataclass definition
├── data/            # Auto-created at first run (contains users.db)
│   └── users.db     # SQLite database file (created automatically)
├── design.drawio    # Visual function-call flowchart (open with draw.io)
├── README.md        # This file
└── requirements.txt # Dependencies list (standard library only)
```

---

## Module-by-Module Breakdown

### 1. `main.py` — UI Layer (Entry Point)

**Purpose:** Handles everything the user sees and interacts with.

**Key functions:**

| Function | Role |
|----------|------|
| `main()` | Infinite loop — shows menu, reads user choice, dispatches to the correct screen function |
| `print_header(title)` | Prints a decorative `==== Title ====` banner |
| `pause()` | Waits for Enter; catches `Ctrl+C` for clean exit |
| `prompt_choice(options)` | Displays a numbered list, returns the user's selection (1-based) |
| `screen_register()` | Prompts for name, DOB, email, password, security question → calls `auth.register()` |
| `screen_login()` | Prompts for email + password → calls `auth.login()` |
| `screen_forgot_password()` | Two-step flow: (1) enter email → show question, (2) answer + new password → calls `auth.reset_password()` |
| `screen_list_users()` | Calls `database.all_users()` and displays every account |
| `screen_exit()` | Prints goodbye message and calls `sys.exit(0)` |

**Dispatch mechanism:**  
The `MENU_ACTIONS` dictionary maps option numbers to functions:  
```python
MENU_ACTIONS = {1: screen_register, 2: screen_login, ...}
```
This is cleaner than a long `if-elif` chain.

### 2. `auth.py` — Business Logic Layer

**Purpose:** Contains all the decision-making logic. It doesn't talk to the user directly — it receives data from `main.py`, validates it, and stores/retrieves it via `database.py`.

**Key functions:**

| Function | Parameters | Returns | What it does |
|----------|-----------|---------|-------------|
| `register(...)` | full_name, dob, email, password, secret_question, secret_answer | `(bool, str, User\|None)` | Validates all fields, hashes password, stores user in DB |
| `login(...)` | email, password | `(bool, str, User\|None)` | Looks up user, compares hashed passwords |
| `forgot_password(...)` | email | `(bool, str, User\|None, str\|None)` | Verifies email, returns the stored security question |
| `reset_password(...)` | email, answer, new_password | `(bool, str)` | Verifies answer, hashes new password, updates DB |

**Constant:** `SECURITY_QUESTIONS` — a list of 5 predefined questions the user picks from during registration.

### 3. `database.py` — Persistence Layer

**Purpose:** All SQLite database operations. Every function follows the pattern:  
`open connection → execute SQL → commit (if needed) → close connection`  
The `try...finally` block ensures the connection is always closed, even on errors.

**Key functions:**

| Function | SQL Statement | Purpose |
|----------|-------------|---------|
| `create_user(user)` | `INSERT INTO users ...` | Adds a new row, returns user with auto-generated ID |
| `get_user_by_email(email)` | `SELECT * FROM users WHERE email = ?` | Looks up a user |
| `get_user_by_id(user_id)` | `SELECT * FROM users WHERE user_id = ?` | Looks up a user by ID |
| `update_password(email, pw)` | `UPDATE users SET password = ? WHERE email = ?` | Changes password |
| `email_exists(email)` | `SELECT 1 FROM users WHERE email = ?` | Checks if email is taken (uses `SELECT 1` for efficiency) |
| `all_users()` | `SELECT * FROM users ORDER BY user_id` | Returns all users |

**Private helper functions:**
- `_get_connection()` — Opens or creates the `.db` file and ensures the `users` table exists.
- `_init_table(conn)` — Runs `CREATE TABLE IF NOT EXISTS` to define the schema.
- `_row_to_user(row)` — Converts a `sqlite3.Row` (dict-like) into a `User` dataclass.

**SQL injection protection:**  
All SQL queries use `?` placeholders instead of string formatting (`f"...{value}..."`). This prevents malicious input from being treated as SQL code.

### 4. `utils.py` — Utility Layer

**Purpose:** Pure helper functions with no side effects — they take input, process it, and return a result. No database access, no user I/O.

**Key functions:**

| Function | Input | Output | What it does |
|----------|-------|--------|-------------|
| `hash_password(password)` | Plain-text string | 64-char hex string | Applies SHA-256 hashing (one-way, irreversible) |
| `validate_email(email)` | String | `bool` | Checks format via regex: `user@domain.suffix` |
| `validate_password(password)` | String | `(bool, str)` | Checks length ≥ 6, has uppercase, has digit |
| `validate_date_of_birth(dob)` | String (YYYY-MM-DD) | `bool` | Parses date, ensures it's in the past |
| `validate_full_name(name)` | String | `bool` | Non-empty, only letters and spaces |
| `format_user_info(user)` | User object | Formatted string | Pretty-prints user details |

### 5. `models.py` — Data Model Layer

**Purpose:** Defines the shape of a user account using Python's `@dataclass` decorator.

```python
@dataclass
class User:
    user_id: int
    full_name: str
    date_of_birth: str
    email: str
    password: str        # This stores the SHA-256 hash, NOT plain text
    secret_question: str
    secret_answer: str

    def to_dict(self) -> dict     # User → dictionary
    @classmethod from_dict(data)  # dictionary → User
```

The `@dataclass` decorator automatically generates `__init__`, `__repr__`, and `__eq__` methods.

### 6. `data/users.db` — SQLite Database File

Created automatically the first time the program runs. Contains a single table:

```
users
├── user_id         INTEGER PRIMARY KEY AUTOINCREMENT
├── full_name       TEXT NOT NULL
├── date_of_birth   TEXT NOT NULL
├── email           TEXT NOT NULL UNIQUE
├── password        TEXT NOT NULL
├── secret_question TEXT NOT NULL
└── secret_answer   TEXT NOT NULL
```

The `UNIQUE` constraint on `email` prevents duplicate registrations.  
The `AUTOINCREMENT` on `user_id` automatically assigns a new ID for each user.

---

## How to Run

### Prerequisites
- Python 3.8 or higher (only standard library needed)
- No external packages required

### Steps

```bash
# 1. Navigate to the project folder
cd MSE800/Week10/Activity_1.1

# 2. Run the program
python main.py
```

---

## Detailed Walkthrough

### First Launch

When you run `python main.py` for the first time:

1. The `data/` directory is automatically created.
2. A new `users.db` SQLite file is created inside it.
3. The `users` table is created inside the database.
4. The main menu appears:

```
============================================================
  User Management CLI
============================================================
  A simple account management system

  [1] Register a new account
  [2] Login
  [3] Forgot password
  [4] List all users
  [5] Exit

  Enter your choice:
```

### Scenario 1: User Registration

1. User selects **[1] Register a new account**.
2. The program prompts for: Full Name, Date of Birth (YYYY-MM-DD), Email, and Password (hidden).
3. The user chooses a security question from a list of 5 and provides an answer.
4. **Validation checks** run automatically:
   - Name: only letters and spaces allowed.
   - DOB: must be a valid date in the past (< today).
   - Email: must match `xxx@yyy.zzz` format.
   - Email uniqueness: checked against the database.
   - Password: at least 6 characters, 1 uppercase letter, 1 digit.
   - Security answer: cannot be empty.
5. If any check fails → an error message is shown (e.g. `❌ Invalid email format.`).
6. If all checks pass:
   - Password is hashed with SHA-256.
   - The user record is inserted into the SQLite database.
   - `✅ Registration successful! Your user ID is 1.` is displayed.

**What gets stored in the database:**
```
user_id:  1
full_name:  Alice Wang
email:      alice@test.com
password:   08fa299aecc0c034e037033e3b0bbfae...  (NOT "Pass123")
```

### Scenario 2: Login

1. User selects **[2] Login**.
2. Enters their email and password (password is hidden).
3. The program:
   - Looks up the email in the database.
   - If not found → `❌ No account found with that email address.`
   - Hashes the entered password and compares it with the stored hash.
   - If mismatch → `❌ Incorrect password.`
   - If match → `✅ Welcome back, Alice Wang!` and shows the user's profile.
4. Press Enter to return to the main menu.

### Scenario 3: Forgot Password

1. User selects **[3] Forgot password**.
2. **Step 1:** Enters their email.
   - If email not found → `❌ No account found with that email address.`
   - If found → displays the security question (e.g. "What is your mother's maiden name?").
3. **Step 2:** User enters:
   - Their answer to the security question.
   - A new password.
4. The program:
   - Compares the answer (case-insensitive) with the stored answer.
   - If wrong → `❌ Incorrect answer to the security question.`
   - If correct → validates the new password strength, hashes it, updates the database.
   - `✅ Password has been reset successfully!`
5. The user can now log in with the new password. The old password no longer works.

### Scenario 4: List Users

1. User selects **[4] List all users**.
2. If no users exist → `No users registered yet.`
3. If users exist → shows each user's info:

```
  ID:          1
  Full Name:   Alice Wang
  Date of Birth: 2000-05-15
  Email:       alice@test.com
----------------------------------------

  ID:          2
  Full Name:   Bob Zhang
  Date of Birth: 1995-08-20
  Email:       bob@test.com
----------------------------------------
```

### Scenario 5: Exit

- User selects **[5] Exit** → `Thank you for using User Management CLI. Goodbye!`
- User presses **`Ctrl+C`** at any prompt → same clean exit, no error traceback.

---

## Expected Outputs

### Successful Registration

```
============================================================
  Register a New Account
============================================================
  Full Name: Alice Wang
  Date of Birth (YYYY-MM-DD): 2000-05-15
  Email: alice@test.com
  Password:
  --- Security Question (for password reset) ---
  [1] What is your mother's maiden name?
  [2] What was the name of your first pet?
  [3] What city were you born in?
  [4] What is your favourite book?
  [5] What is the model of your first car?

  Choose a question (1-5): 1
  Your answer: Fluffy

  ✅ Registration successful! Your user ID is 1.

  Press Enter to continue...
```

### Failed Registration (Duplicate Email)

```
  ❌ An account with this email already exists.

  Press Enter to continue...
```

### Successful Login

```
============================================================
  Login
============================================================
  Email: alice@test.com
  Password:

  ✅ Welcome back, Alice Wang!

  Your profile:
    ID:          1
    Full Name:   Alice Wang
    Date of Birth: 2000-05-15
    Email:       alice@test.com

  Press Enter to continue...
```

### Forgot Password — Complete Flow

```
============================================================
  Forgot Password
============================================================
  Email: alice@test.com

  Security question: What is your mother's maiden name?
  Your answer: Fluffy
  New password:

  ✅ Password has been reset successfully!

  Press Enter to continue...
```

---

## Architecture & Design Principles

### Layered Architecture

```
┌─────────────────────────────────────────────────────────┐
│  main.py           (UI Layer)                           │
│  ──────────────                                          │
│  Only layer that interacts with the user.               │
│  Handles menus, input, output.                          │
├─────────────────────────────────────────────────────────┤
│  auth.py           (Business Logic Layer)                │
│  ──────────────                                          │
│  Validates data, enforces rules, orchestrates workflows. │
│  Never reads input or prints to screen directly.        │
├─────────────────────────────────────────────────────────┤
│  database.py      (Persistence Layer)                    │
│  utils.py         (Utility Layer)                        │
│  ──────────────                                          │
│  database.py: SQL queries, CRUD operations.              │
│  utils.py:     Hashing, validation, formatting.          │
├─────────────────────────────────────────────────────────┤
│  models.py        (Data Model Layer)                     │
│  ──────────────                                          │
│  Defines User class — the shape of the data.             │
├─────────────────────────────────────────────────────────┤
│  data/users.db    (Physical Storage)                     │
│  ──────────────                                          │
│  The actual SQLite file on disk.                         │
└─────────────────────────────────────────────────────────┘
```

### Dependency Rule

> **Upper layers can call lower layers, but lower layers NEVER call upper layers.**

- ✅ `main.py` → calls → `auth.py`
- ✅ `auth.py` → calls → `database.py`, `utils.py`, `models.py`
- ✅ `database.py` → uses → `models.py` (User class)
- ❌ `utils.py` cannot import `main.py`
- ❌ `models.py` cannot import `database.py`

This ensures that changing one layer doesn't break the layers above it.

### Key Design Decisions

| Decision | Why |
|----------|-----|
| **SQLite instead of JSON** | SQLite is a real database with ACID transactions, UNIQUE constraints, and indexed lookups — all while being built into Python's standard library. |
| **SHA-256 hashing** | Passwords are never stored in plain text. Even if the `.db` file is stolen, the original passwords cannot be recovered. |
| **`?` placeholders in SQL** | Prevents SQL injection — a common vulnerability where malicious input manipulates SQL queries. |
| **`try...finally` for DB connections** | Guarantees the connection is closed even if an error occurs, preventing resource leaks. |
| **Dictionary dispatch** (`MENU_ACTIONS`) | Maps menu numbers directly to functions, much cleaner than a long `if-elif-elif` chain. |
| **Tuple return values** | Every `auth.py` function returns `(success, message, ...)` — the UI layer just checks `if success:` and prints the message, no complex error handling needed. |
| **`getpass` for password input** | Passwords are not echoed on screen, preventing shoulder-surfing. |
| **`KeyboardInterrupt` handling** | `Ctrl+C` at any prompt exits cleanly instead of showing a Python traceback. |

---

## Security Features

| Concern | Solution |
|---------|----------|
| **Password visible on screen** | `getpass.getpass()` hides input |
| **Password stored in plain text** | `hashlib.sha256()` hashes before storage |
| **SQL injection attacks** | `?` placeholders in all SQL queries |
| **Duplicate email registrations** | `UNIQUE` constraint in the database schema |
| **Brute-force password guessing** | Password strength validation (length + uppercase + digit) |
| **Forgot password without identity verification** | Security question must be answered correctly |

**Note:** This is a classroom project. For a production system, you would add:
- Salted password hashing (bcrypt/argon2)
- Rate limiting on login attempts
- Email verification
- Session management
- HTTPS for network communication

---

## Requirements

See `requirements.txt`.  
This project uses **only Python standard library modules**:

- `sqlite3` — Embedded relational database
- `hashlib` — SHA-256 password hashing
- `getpass` — Hidden password input
- `re` — Regular expressions for email validation
- `datetime` — Date parsing and validation
- `dataclasses` — User data class
- `pathlib` — Cross-platform file paths
- `typing` — Type annotations

**No third-party packages required.**  
Python 3.8+ recommended.
