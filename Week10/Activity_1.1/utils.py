"""
utils.py — Utility & validation functions

Contains small, reusable helper functions used across the application.
Each function does exactly one thing:
1. Single responsibility — each function focuses on one task
2. Reusable — registration, login, etc. all use these validators
3. Independent — no interaction with the database or UI

Centralising validation here keeps auth.py clean and avoids code duplication.
"""

# hashlib:  provides hash algorithms (turns passwords into irreversible "fingerprints")
# re:       regular expressions (email format checking)
# datetime: date and time handling
import hashlib
import re
from datetime import datetime


def hash_password(password: str) -> str:
    """
    Hash a plain-text password using SHA-256.

    What is hashing?
    Think of a "juicer" — you put in an apple and get apple juice.
    You can't turn apple juice back into a whole apple.
    Similarly, hashlib.sha256() turns a password into a fixed string
    that cannot be reversed to recover the original password.

    Steps:
    1. password.encode()     → convert string to bytes (computer-readable format)
    2. hashlib.sha256(...)   → compute SHA-256 hash
    3. .hexdigest()          → convert to 64-character hexadecimal string

    Example:
    hash_password("Pass123")
    → "08fa299aecc0c034e037033e3b0bbfaef26b78c742f16cf88ac3194502d6c394"
    """
    return hashlib.sha256(password.encode()).hexdigest()


def validate_email(email: str) -> bool:
    """
    Check if the email format is valid.

    Uses a regular expression (re module) for pattern matching.
    r"^...$" means match from start to end:
    - ^                 start of string
    - [a-zA-Z0-9_.+-]+  local part (letters, digits, underscore, dot, plus, hyphen)
    - @                 must contain @
    - [a-zA-Z0-9-]+     domain name part
    - \\.               dot separator
    - [a-zA-Z0-9-.]+$   domain suffix, end of string

    Returns True if valid, False otherwise.
    """
    # Pattern: username@domain.suffix (e.g. alice@example.com)
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    # re.match() tries to match from the start of the string
    # Returns a Match object if found (!= None → True)
    # Returns None if no match (== None → False)
    return re.match(pattern, email) is not None


def validate_date_of_birth(dob: str) -> bool:
    """
    Validate a date of birth string.

    Requirements:
    1. Must be in YYYY-MM-DD format (e.g. 2000-01-15)
    2. Must be a real date (no such thing as 2023-13-01)
    3. Cannot be in the future

    datetime.strptime():
    strptime = "string parse time"
    First arg is the string, second arg is the format template.
    %Y = 4-digit year, %m = 2-digit month, %d = 2-digit day
    """
    try:
        # Try to parse the string "2000-01-15" into a datetime object
        # If the format is wrong (e.g. "abc"), a ValueError is raised
        dt = datetime.strptime(dob, "%Y-%m-%d")

        # Check the date is not in the future
        # datetime.now() gets the current date and time
        return dt <= datetime.now()
    except ValueError:
        # Parse failed → wrong format or invalid date → return False
        return False


def validate_password(password: str) -> tuple:
    """
    Check password strength.

    Returns a tuple (is_valid, message):
    - (True, "OK")                         — password is strong enough
    - (False, "explanation...")            — too weak, with reason

    Rules:
    1. Minimum 6 characters
    2. At least one uppercase letter
    3. At least one digit

    any(): returns True if at least one element in the iterable is True.
    c.isupper(): checks if character c is an uppercase letter.
    c.isdigit(): checks if character c is a digit.
    """
    # Check minimum length
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    # Check for at least one uppercase letter
    # Iterates through each character c in password
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter."

    # Check for at least one digit
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit."

    # All checks passed
    return True, "OK"


def validate_full_name(name: str) -> bool:
    """
    Validate a full name.

    Requirements:
    1. Cannot be empty
    2. Each word must consist only of letters (no digits or special chars)

    name.split() splits "Alice Wang" into ["Alice", "Wang"]
    part.isalpha() checks if a part is entirely alphabetic
    all(): returns True only if EVERY element is True
    """
    # bool(name): check the name is not an empty string
    # all(...):   check every word is made of letters only
    return bool(name) and all(part.isalpha() for part in name.split())


def format_user_info(user) -> str:
    """
    Format a User object into a readable multi-line string for display.

    Args:
        user: A User object

    Returns:
        Formatted string:
          ID:          1
          Full Name:   Alice Wang
          Date of Birth: 2000-01-15
          Email:       alice@test.com
    """
    lines = [
        f"  ID:          {user.user_id}",
        f"  Full Name:   {user.full_name}",
        f"  Date of Birth: {user.date_of_birth}",
        f"  Email:       {user.email}",
    ]
    # "\n".join(lines) concatenates list elements with newline characters
    return "\n".join(lines)
