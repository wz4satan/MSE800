# Import two decorators.
from decorators import administor_log, animals_info_manage

@administor_log
# Use no argument, for the main function can use the argument passed from decorators.
def admin_login():
    print("Let's start to work.")
  
@animals_info_manage
def check_animals_status(username):
    print(f"{username} is checking animals' status.")
    
