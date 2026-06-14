"""
main.py — CLI entry point (this is where the program starts)

This file is the "front door" — when a user runs `python main.py`,
execution begins in the main() function below.

Responsibilities:
1. Display menus and prompts (UI layer)
2. Read user input
3. Call functions in auth.py to handle business logic
4. Display results to the user

Architecture (call chain):
main.py     (UI layer — only talks to the user)
    |
    v
auth.py     (business logic layer — makes decisions)
    |
    v
models.py  ->  database.py  ->  utils.py
(data def.)   (persistence)   (validation)

Run with:
    python main.py
"""

# getpass: password input module (hides input on screen)
import getpass

# sys: system module, used here to exit the program (sys.exit)
import sys

# Import required functions and constants from auth.py
from auth import (
    SECURITY_QUESTIONS,  # List of security questions
    forgot_password,  # Forgot password flow
    login,  # User login
    register,  # User registration
    reset_password,  # Password reset
)

# Import function to list all users from database.py
from database import all_users

# Import function to format user info from utils.py
from utils import format_user_info

# ===================================================================
# Menu helper functions
# These handle "display" and "input" — they don't touch business logic
# ===================================================================


def print_header(title: str) -> None:
    """
    Print a decorative section header.

    Output:
    ============================================================
      Title Text
    ============================================================

    Args:
        title: The text to display as the header
    """
    width = 60
    print()
    print("=" * width)
    print(f"  {title}")
    print("=" * width)


def pause() -> None:
    try:
        input("\n  Press Enter to continue...")
    except KeyboardInterrupt:
        screen_exit()


def prompt_choice(options: list) -> int:
    for i, opt in enumerate(options, 1):
        print(f"  [{i}] {opt}")

    print()

    try:
        # Read user input and convert to integer
        choice = int(input("  Enter your choice: "))

        # Check if the choice is within valid range
        if 1 <= choice <= len(options):
            return choice

        # Out of range → invalid
        print("  Invalid choice. Please try again.")

    except ValueError:
        # int() conversion failed (user typed a non-number)
        print("  Please enter a number.")

    except KeyboardInterrupt:
        # User pressed Ctrl+C → exit
        screen_exit()

    # Only reached on invalid input — return 0 for "invalid"
    return 0


# ===================================================================
# Feature screens
# Each screen_xxx function corresponds to one menu option.
# These functions only:
#   1. Display prompts → 2. Read input → 3. Call auth.py → 4. Show result
# ===================================================================


def screen_register() -> None:
    """Register a new account: prompt for info, validate, store in DB."""
    print_header("Register a New Account")

    # .strip() removes leading/trailing whitespace
    fn = input("  Full Name: ").strip()
    dob = input("  Date of Birth (YYYY-MM-DD): ").strip()
    email = input("  Email: ").strip()

    # getpass.getpass() works like input() but doesn't show what you type on the screen at all — it hides the input for privacy
    password = getpass.getpass("  Password: ")

    # Show security question list
    print("\n  --- Security Question (for password reset) ---")
    for i, q in enumerate(SECURITY_QUESTIONS, 1):
        print(f"  [{i}] {q}")

    try:
        q_choice = int(input("\n  Choose a question (1-5): "))
        if q_choice < 1 or q_choice > 5:
            print("  Invalid choice. Returning to menu.")
            return
    except ValueError:
        print("  Invalid input. Returning to menu.")
        return

    # Get the selected question text
    q = SECURITY_QUESTIONS[q_choice - 1]
    a = input("  Your answer: ").strip()

    # Call auth.py's register() function
    # Returns (success, message, User_object)
    success, msg, _ = register(fn, dob, email, password, q, a)

    # Display result
    print(f"\n  {'✅' if success else '❌'} {msg}")
    pause()


def screen_login() -> None:
    print_header("Login")

    email = input("  Email: ").strip()
    password = getpass.getpass("  Password: ")

    # Call auth.py's login() for authentication
    success, msg, user = login(email, password)

    # Show result
    print(f"\n  {'✅' if success else '❌'} {msg}")

    # If login succeeded, show user details
    if success and user:
        print(f"\n  Your profile:\n{format_user_info(user)}")

    pause()


def screen_forgot_password() -> None:
    print_header("Forgot Password")

    # Step 1: Enter email
    email = input("  Email: ").strip()

    # Call forgot_password() to verify the email
    # Returns 4 values: (success, message, user_object, security_question)
    success, msg, _, question = forgot_password(email)

    if not success:
        # Email not found → inform user and return to menu
        print(f"\n  ❌ {msg}")
        pause()
        return

    # Email found → show security question
    print(f"\n  Security question: {question}")

    # Step 2: Answer the question
    answer = input("  Your answer: ").strip()
    new_pw = getpass.getpass("  New password: ")

    # Call reset_password() to verify answer and set new password
    success, msg = reset_password(email, answer, new_pw)

    # Show result
    print(f"\n  {'✅' if success else '❌'} {msg}")
    pause()


def screen_list_users() -> None:
    print_header("All Registered Users")

    # Call database.py's all_users() to get all users
    users = all_users()

    if not users:
        # No users yet
        print("\n  No users registered yet.")
    else:
        # Iterate and display each user
        for u in users:
            print()
            print(format_user_info(u))
            print("-" * 40)

    pause()


def screen_exit() -> None:
    print("\n  Thank you for using User Management CLI. Goodbye!\n")
    sys.exit(0)


# ===================================================================
# Main loop
# The program loops here after starting, until the user chooses "Exit"
# or presses Ctrl+C.
# ===================================================================

# Menu options shown to the user
MENU_OPTIONS = [
    "Register a new account",  # 1
    "Login",  # 2
    "Forgot password",  # 3
    "List all users",  # 4
    "Exit",  # 5
]

# Map menu numbers to their corresponding functions
# Option 1 -> screen_register(), Option 2 -> screen_login(), etc.
# This dictionary mapping is cleaner than writing if...elif...elif...
MENU_ACTIONS = {
    1: screen_register,
    2: screen_login,
    3: screen_forgot_password,
    4: screen_list_users,
    5: screen_exit,
}


def main() -> None:
    """Program entry point: show menu, dispatch actions, loop until exit."""
    while True:
        try:
            # Show the main menu header
            print_header("User Management CLI")
            print("  A simple account management system\n")

            # Get the user's menu selection (1-5)
            choice = prompt_choice(MENU_OPTIONS)

            # Look up the corresponding function
            # .get(choice) returns the function if found, or None if not
            action = MENU_ACTIONS.get(choice)

            if action:
                # Found the function → execute it
                # action is a function reference, action() calls it
                action()
            else:
                # No matching function → show error
                print("  Invalid choice. Please try again.")
                pause()

        except KeyboardInterrupt:
            # User pressed Ctrl+C → exit cleanly
            screen_exit()


# ===== Program starts executing from here =====

# The meaning of if __name__ == "__main__":
# Every Python file has a built-in variable __name__.
# When run directly (python main.py), __name__ equals "__main__".
# When imported by another file (from main import ...), __name__ equals "main".
# This line means: "If I'm being run directly, call main()."
if __name__ == "__main__":
    main()
