from datetime import datetime
# Import datetime from datetime lib

def log_activity(func): # Definite the log_activity as a Decorator

    def wrapper(*args, **kwargs):
        print("===================================")
        print(f"Function: {func.__name__}")
        print(f"Time: {datetime.now()}")
        print("Activity started...")

        result = func(*args, **kwargs)
        # Use 'result' as a variable to store the function 'func'. 
        
        print("Activity completed.")
        print("===================================\n")
        return result
        # Return 'result' to anyone who calling this Decorator.

    return wrapper
    # Return 'wrapper' to system or IDE.
