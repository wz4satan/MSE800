from datetime import datetime
# Set the right admin_name and password.
admin_name = "ZheWang"
admin_password = "abc12345678"

# Definite the first decorator for login behavior.
def administor_log(func):
    
    def wrapper(*args, **kwargs):
        
        print("===================================")
        print(f"Function: {func.__name__}")
        print("===================================")
        print("Please enter your Admin name and Password.\n")
        # Put input behavior in decorators to simplify the other module.
        input_username = input("Admin name: ")
        input_password = input("Password: ")
    
        #Compare the input parameters than the setted ones.
        if input_username == admin_name and input_password == admin_password:
            print("\nWelcome.\n")
            print(f"{input_username}, your punch in time is {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}.")
            print("Enjoy your day!")
            
            func(*args, **kwargs)
            
            # ! Return the input name to the main function to make sure that, under this condition, the "name" is not None.
            return input_username
        else:
            print("\nInvalid password or admin name, please check.\n")
            return None    
        
    return wrapper

def animals_info_manage(func):
    
    def wrapper(*args, **kwargs):
        print("===================================")
        print(f"Function: {func.__name__}")
        print("===================================")
        print(f"Right now, it is {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}.")
  
        result = func(*args, **kwargs)
        
        print("===================================\n")
        
        return result

    return wrapper

        
        
        
        
        
        
            
    