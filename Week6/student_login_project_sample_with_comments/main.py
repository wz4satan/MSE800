from users import (
    student_login,
    submit_assignment,
    view_grades
)
# Import these three functions from 'users' file.


def main():
    # Execute the following functions in sequence.
    student_login("Mohammad")

    submit_assignment(
        "Mohammad",
        "Python Decorator Project"
    )

    view_grades("Alex") # Warning: Logically, 'Alex' comes from nowhere without login.
    # Here should be the same person as before.

if __name__ == "__main__":
    main()
