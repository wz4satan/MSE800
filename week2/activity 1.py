import math

def basic_operations(a, b):
    """
    Function 1: Performs basic mathematical operations (+, -, *, /, %)
    Supports integers, floats, and complex numbers.
    """
    results = {}
    
    # Addition, Subtraction, Multiplication
    results['+'] = a + b
    results['-'] = a - b
    results['*'] = a * b
    
    # Division (with zero-division error handling)
    if b != 0:
        results['/'] = a / b
    else:
        results['/'] = "Error: Division by zero"
        
    # Modulo % (executed only if neither number is a complex number)
    if not isinstance(a, complex) and not isinstance(b, complex):
        if b != 0:
            results['%'] = a % b
        else:
            results['%'] = "Error: Modulo by zero"
    else:
        results['%'] = "N/A (Unsupported for complex types)"
        
    return results

def calculate_factorial(n):
    """
    Function 2: Calculates the factorial of a number.
    Only supports non-negative integers.
    """
    if isinstance(n, int) and n >= 0:
        return math.factorial(n)
    else:
        return "Error: Factorial requires a non-negative integer."

def get_number_input(prompt):
    """
    Function 3: Safely gets numeric input from the user.
    Handles integers, floats, and complex numbers (e.g., 2+3j).
    """
    while True:
        user_input = input(prompt).strip()
        try:
            # Try parsing as a complex number if 'j' is in the input
            if 'j' in user_input:
                return complex(user_input.replace(' ', ''))
            
            # Otherwise, parse as a float
            num = float(user_input)
            
            # If it is a whole number, convert it to an int (helps with the factorial function)
            if num.is_integer():
                return int(num)
                
            return num
        except ValueError:
            print("Invalid input. Please enter a valid number (e.g., 5, 3.2, or 2+3j).")

def main():
    """
    Function 4: Main program entry point for user interaction.
    """
    print("=== Mathematical Operations Program ===")
    print("Note: For complex numbers, use 'j' for the imaginary part (e.g., 2+3j or 5j).\n")
    
    # 1. Get user inputs for basic operations
    print("--- Basic Operations ---")
    num1 = get_number_input("Enter the first number: ")
    num2 = get_number_input("Enter the second number: ")
    
    print(f"\nCalculating results for ({num1}) and ({num2})...")
    ops_result = basic_operations(num1, num2)
    for op, res in ops_result.items():
        print(f"({num1}) {op} ({num2}) = {res}")
        
    # 2. Get user input for factorial
    print("\n--- Factorial Calculation ---")
    fact_num = get_number_input("Enter a non-negative integer for factorial: ")
    print(f"Factorial result -> {fact_num}! = {calculate_factorial(fact_num)}")

if __name__ == "__main__":
    main()