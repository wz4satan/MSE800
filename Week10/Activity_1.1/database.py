"""
database.py — SQLite database layer (Python built-in)

Handles all data persistence using Python's built-in sqlite3 module.
No external packages required — SQLite stores everything in a single .db file.

Table structure (users):

    Column          | Type    | Description
    ----------------+---------+---------------------------------
    user_id         | INTEGER | Primary key, auto-incremented
    full_name       | TEXT    | User's full name
    date_of_birth   | TEXT    | Date of birth (YYYY-MM-DD)
    email           | TEXT    | Email address (UNIQUE)
    password        | TEXT    | Password hash (SHA-256)
    secret_question | TEXT    | Security question
    secret_answer   | TEXT    | Answer to security question
"""

# sqlite3: Python's built-in database module (no pip install needed)
import sqlite3

# Path: cross-platform file path handling
from pathlib import Path

# List, Optional: type hints for better code readability
from typing import List, Optional

# Import the User dataclass from models.py
from models import User

# __file__ is the full path to this file (database.py)
# .parent goes up one directory to the Activity_1.1 folder
# The database file is stored at Activity_1.1/data/users.db
DB_DIR = Path(__file__).parent / "data"  # database directory
DB_FILE = DB_DIR / "users.db"  # database file path


# ---------------------------------------------------------------------------
# Database connection & initialization
# (Names starting with _ are "private" — used only inside this file)
# ---------------------------------------------------------------------------


def _get_connection() -> sqlite3.Connection:
    """
    Open a connection to the SQLite database.

    Every call to this function:
    1. Ensures the data/ directory exists (creates it if needed).
    2. Connects to (or creates) the users.db file.
    3. Ensures the users table exists (creates it if needed).
    4. Returns the connection object.

    A Connection is the "channel" to the database — you need it to
    execute any SQL statements.
    """
    # mkdir(parents=True) creates parent directories recursively
    # exist_ok=True means no error if the directory already exists
    DB_DIR.mkdir(parents=True, exist_ok=True)

    # connect() opens (or creates) the database file
    conn = sqlite3.connect(str(DB_FILE))

    # row_factory = sqlite3.Row:
    # By default, query results are returned as tuples (1, "Alice", ...).
    # With this setting, you can access columns by name: row["email"]
    # This is much more readable, like a dictionary.
    conn.row_factory = sqlite3.Row

    # Make sure the table exists
    _init_table(conn)

    return conn


def _init_table(conn: sqlite3.Connection) -> None:
    """
    Create the users table if it doesn't exist yet.

    SQL keywords explained:
    - CREATE TABLE IF NOT EXISTS: create only if missing
    - INTEGER PRIMARY KEY AUTOINCREMENT: auto-incrementing integer ID
      (each new record gets ID = previous max + 1)
    - TEXT NOT NULL: text field that cannot be empty
    - UNIQUE: no two rows can have the same value in this column
    """
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id         INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name       TEXT    NOT NULL,
            date_of_birth   TEXT    NOT NULL,
            email           TEXT    NOT NULL UNIQUE,
            password        TEXT    NOT NULL,
            secret_question TEXT    NOT NULL,
            secret_answer   TEXT    NOT NULL
        )
    """)
    # Note: CREATE TABLE doesn't need conn.commit(), but INSERT/UPDATE/DELETE does


def _row_to_user(row: sqlite3.Row) -> User:
    """
    Convert a database row into a User object.

    The database returns sqlite3.Row objects (dict-like).
    We convert them to User dataclass instances for cleaner Python usage.
    row["user_id"] retrieves the value of the user_id column.
    """
    return User(
        user_id=row["user_id"],
        full_name=row["full_name"],
        date_of_birth=row["date_of_birth"],
        email=row["email"],
        password=row["password"],
        secret_question=row["secret_question"],
        secret_answer=row["secret_answer"],
    )


# ---------------------------------------------------------------------------
# Public API — called by auth.py
# Each function follows the pattern: open → operate → close
# try...finally guarantees the connection is always closed
# ---------------------------------------------------------------------------


def create_user(user: User) -> User:
    """
    Insert a new user into the database.

    Args:
        user: A User object (user_id is 0 temporarily — the DB assigns the real one).

    Returns:
        The same User object with user_id set to the auto-generated ID.

    Key concepts:
    - INSERT INTO ... VALUES (?, ?, ...): the SQL statement for adding rows
    - ? are "placeholders" that prevent SQL injection attacks
      (never use f"INSERT ... VALUES ({name})" — that's dangerous!)
    - cursor.lastrowid gets the ID of the row we just inserted
    - conn.commit() saves the change permanently to the file
    """
    conn = _get_connection()

    # try...finally ensures conn.close() runs even if an error occurs.
    # This prevents database connection leaks.
    try:
        # execute() runs a SQL statement and returns a cursor object.
        # The cursor tells us about the result (e.g. lastrowid).
        cursor = conn.execute(
            # SQL: insert a new record
            # ? placeholders are replaced by the second argument to execute()
            # This prevents SQL injection — much safer than string formatting.
            """INSERT INTO users
               (full_name, date_of_birth, email, password, secret_question, secret_answer)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                user.full_name,
                user.date_of_birth,
                user.email,
                user.password,  # Note: this is already hashed
                user.secret_question,
                user.secret_answer,
            ),
        )
        # commit() finalises the transaction — without it, data won't be saved
        conn.commit()

        # lastrowid is the auto-generated ID of the record we just inserted
        user.user_id = cursor.lastrowid

        return user
    finally:
        # Always close the connection, whether successful or not
        conn.close()


def get_user_by_email(email: str) -> Optional[User]:
    """
    Find a user by their email address.

    Args:
        email: The email to search for.

    Returns:
        A User object if found, or None if not found.

    SQL notes:
    - SELECT * FROM users: query all columns from the users table
    - WHERE email = ?: only return rows where email matches
    - fetchone(): get the first matching row
      (since email has a UNIQUE constraint, there's at most one match)
    """
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,),
        )
        # fetchone() returns a sqlite3.Row object, or None if no match
        row = cursor.fetchone()

        # if row is not None → convert to User and return it
        return _row_to_user(row) if row else None
    finally:
        conn.close()


def get_user_by_id(user_id: int) -> Optional[User]:
    """
    Find a user by their unique ID.

    Works the same as get_user_by_email, but searches by user_id instead.
    """
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "SELECT * FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        return _row_to_user(row) if row else None
    finally:
        conn.close()


def update_password(email: str, new_password: str) -> bool:
    """
    Update the password for the user identified by email.

    Args:
        email:        The user's email address
        new_password: The new password hash (already hashed, not plain-text)

    Returns:
        True  — update successful
        False — user not found

    SQL notes:
    - UPDATE users SET ... WHERE ...: modify rows matching the condition
    - cursor.rowcount: number of rows affected by the statement
      > 0 means something was updated; = 0 means no match
    """
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "UPDATE users SET password = ? WHERE email = ?",
            (new_password, email),
        )
        conn.commit()
        # rowcount > 0 means at least one row was updated
        return cursor.rowcount > 0
    finally:
        conn.close()


def email_exists(email: str) -> bool:
    """
    Check whether an email is already registered.

    Tip:
    - We use "SELECT 1" instead of "SELECT *"
      because we only care about existence, not the actual data.
    - "SELECT 1" returns (1,) if a match is found.
    - If fetchone() is not None → email exists; if None → email is available.
    """
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "SELECT 1 FROM users WHERE email = ?",
            (email,),
        )
        # Not None → exists; None → available
        return cursor.fetchone() is not None
    finally:
        conn.close()


def all_users() -> List[User]:
    """
    Get a list of every registered user.

    SQL notes:
    - SELECT * FROM users: get all users
    - ORDER BY user_id: sort by user ID ascending

    Returns a list of User objects.
    The list comprehension [func(x) for x in items] transforms each row.
    """
    conn = _get_connection()
    try:
        cursor = conn.execute("SELECT * FROM users ORDER BY user_id")
        # fetchall() gets all rows, returns a list
        # The list comprehension converts each row to a User object
        return [_row_to_user(row) for row in cursor.fetchall()]
    finally:
        conn.close()
