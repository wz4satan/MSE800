from decorators import log_activity
# Import 'log_activity' from Decorators.
 

# Definite functions by calling the Decorators to change the functions.
@log_activity
def student_login(username):
    print(f"{username} logged into the system.")


@log_activity
def submit_assignment(username, assignment):
    print(f"{username} submitted {assignment}.")


@log_activity
def view_grades(username):
    print(f"{username} is viewing grades.")
