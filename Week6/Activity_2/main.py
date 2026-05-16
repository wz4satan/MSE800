from users_functions import admin_login, check_animals_status

def main():
    # Use "user" as a variable to store the value of "admin_login()", which is returned by the decorator.
    user = admin_login()
    
    if user is not None:
        check_animals_status(user)
    else:
        print("For the further operations, you can't perform them without login.")
    
if __name__== "__main__":
    main()