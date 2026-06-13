"""
models.py — Data model (User class)

Defines the User dataclass that represents a user account.
This is the blueprint for what data a user has — like a spreadsheet header
defining each column name and its type.

@dataclass is Python's built-in decorator that automatically generates
__init__, __repr__, and other boilerplate methods.
"""

# dataclass:  generates constructors, __repr__, etc. automatically
# asdict:     converts a dataclass instance into a plain dictionary
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class User:
    """
    Data model for a user account.

    Every registered user is stored as a User object containing
    their personal info and authentication credentials.

    Fields:
        user_id:         Unique ID assigned by the database (auto-increment).
        full_name:       User's full name.
        date_of_birth:   Date of birth in YYYY-MM-DD format (e.g. 2000-01-15).
        email:           Email address, also used as login ID.
        password:        Password hash (not the plain-text password).
        secret_question: Security question for password reset.
        secret_answer:   Answer to the security question.
    """

    user_id: int
    full_name: str
    date_of_birth: str
    email: str
    password: str
    secret_question: str
    secret_answer: str

    def to_dict(self) -> dict:
        """
        Convert the User object to a dictionary.

        A dict is Python's {key: value} format, useful for
        serialization or passing data to other functions.
        """
        # asdict() from dataclasses module automatically
        # converts all fields into a dictionary
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """
        Create a User object from a dictionary.
        This is the inverse of to_dict().

        @classmethod means this is a class method — you call it
        directly as User.from_dict(...) without creating an object first.
        **data unpacks the dictionary into keyword arguments,
        e.g. User(**{"name": "Alice"}) becomes User(name="Alice").
        """
        return cls(**data)
