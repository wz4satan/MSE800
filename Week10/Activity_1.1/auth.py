"""
auth.py — Business logic layer (registration, login, forgot password)

This file acts as the "middleman" — connecting main.py (UI) and database.py (data).

Responsibilities:
1. Receive user input from main.py
2. Call utils.py for format validation
3. Call database.py to read/write data
4. Tell main.py whether the operation succeeded or failed

Every function returns a tuple (success, message, ...)
so main.py can display the result directly to the user.
"""

# Import the User dataclass from models.py
from models import User

# Import database operations from database.py
from database import (
    create_user,  # Insert a new user
    get_user_by_email,  # Look up a user by email
    update_password,  # Update a user's password
    email_exists,  # Check if an email is already registered
)

# Import utility functions from utils.py
from utils import (
    hash_password,  # Hash a plain-text password
    validate_email,  # Check email format
    validate_password,  # Check password strength
    validate_date_of_birth,  # Check date of birth validity
    validate_full_name,  # Check full name validity
)

# ---------------------------------------------------------------------------
# Security questions list
# Users pick one during registration; it's used to verify identity
# when they forget their password.
# ---------------------------------------------------------------------------

SECURITY_QUESTIONS = [
    "What is your mother's maiden name?",
    "What was the name of your first pet?",
    "What city were you born in?",
    "What is your favourite book?",
    "What is the model of your first car?",
]


def register(
    full_name: str,
    date_of_birth: str,
    email: str,
    password: str,
    secret_question: str,
    secret_answer: str,
) -> tuple:
    """
    Register a new user account.

    Steps:
    1. Validate all inputs for correctness
    2. Check if the email is already taken
    3. Hash the password
    4. Store the user in the database

    Returns:
        (success: bool, message: str, user: User | None)
    """
    # ====== Step 1: Data validation ======

    # Check name: must not be empty, letters and spaces only
    if not validate_full_name(full_name):
        return False, "Invalid full name — use only letters and spaces.", None

    # Check date of birth: must be valid and not in the future
    if not validate_date_of_birth(date_of_birth):
        return (
            False,
            "Invalid date of birth — use YYYY-MM-DD and ensure it is in the past.",
            None,
        )

    # Check email format
    if not validate_email(email):
        return False, "Invalid email format.", None

    # Check if email is already registered
    if email_exists(email):
        return False, "An account with this email already exists.", None

    # Check password strength
    valid_pw, pw_msg = validate_password(password)
    if not valid_pw:
        return False, pw_msg, None

    # Check security answer is not empty
    if not secret_answer.strip():
        return False, "Security answer cannot be empty.", None

    # ====== Step 2: Store in database ======

    # Create a User object
    # user_id=0 is temporary — create_user() will assign the real ID
    user = User(
        user_id=0,  # Temporary ID, DB re-assigns it
        full_name=full_name.strip(),  # Remove leading/trailing spaces
        date_of_birth=date_of_birth,
        email=email.strip().lower(),  # Lowercase (avoids Alice@Test == alice@test confusion)
        password=hash_password(password),  # Key! Store hash, NOT plain-text
        secret_question=secret_question,
        secret_answer=secret_answer.strip().lower(),  # Lowercase for case-insensitive comparison
    )

    # Call database.py to write the user data into SQLite
    saved = create_user(user)

    # Return success message with the assigned user ID
    return True, f"Registration successful! Your user ID is {saved.user_id}.", saved


def login(email: str, password: str) -> tuple:
    """
    Authenticate a user login.

    Steps:
    1. Look up the user by email
    2. If not found → "email not registered"
    3. Hash the input password, compare with stored hash
    4. Hash mismatch → "incorrect password"
    5. Match → login successful

    Why compare hashes instead of plain-text?
    The database stores the hash "08fa...394", not "Pass123".
    So we hash the user's input and compare the two hashes.
    """
    user = get_user_by_email(email.strip().lower())

    # Not found → email not registered
    if user is None:
        return False, "No account found with that email address.", None

    # Hash comparison: hash the input, then compare
    if user.password != hash_password(password):
        return False, "Incorrect password.", None

    # All checks passed → login successful
    return True, f"Welcome back, {user.full_name}!", user


def forgot_password(email: str) -> tuple:
    """
    Forgot password — Step 1: verify email, return security question.

    Steps:
    1. Check if the email is registered
    2. If found, return the user's security question

    Returns 4 values:
        (success: bool, message: str, user: User | None, question: str | None)
    """
    user = get_user_by_email(email.strip().lower())

    # Email not found
    if user is None:
        return False, "No account found with that email address.", None, None

    # User found, return the security question
    return True, "Security question found.", user, user.secret_question


def reset_password(email: str, answer: str, new_password: str) -> tuple:
    """
    Forgot password — Step 2: verify security answer, reset password.

    Steps:
    1. Check if the email exists
    2. Compare the security answer (case-insensitive)
    3. Validate the new password strength
    4. Hash the new password and update the database

    Returns:
        (success: bool, message: str)
    """
    user = get_user_by_email(email.strip().lower())

    # Email not found
    if user is None:
        return False, "No account found with that email address."

    # Compare security answer (stored in lowercase, so convert input too)
    if user.secret_answer != answer.strip().lower():
        return False, "Incorrect answer to the security question."

    # Validate new password strength
    valid_pw, pw_msg = validate_password(new_password)
    if not valid_pw:
        return False, pw_msg

    # Hash the new password and update the database
    update_password(email.strip().lower(), hash_password(new_password))

    return True, "Password has been reset successfully!"
