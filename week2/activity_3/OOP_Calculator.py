import math

class AdvancedCalculator:
    
    def __init__(self):
        # State: Store calculation history in a list
        self.history = []
        
    def perform_basic_math(self, num1, num2, operator):
        # Handle basic mathematical operations
        result = None
        
        try:
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    return "Error: Division by zero is not allowed."
                result = num1 / num2
            elif operator == '%':
                if isinstance(num1, complex) or isinstance(num2, complex):
                    return "Error: Modulo (%) is not supported for complex numbers."
                result = num1 % num2
            else:
                return "Error: Invalid operator."
            
            # Save the successful calculation to history
            equation = f"{num1} {operator} {num2} = {result}"
            self.history.append(equation)
            return result
            
        except Exception as e:
            return f"Unexpected Error: {e}"

    def perform_factorial(self, n):
        # Check if 'n' is valid (complex/floats cannot be directly factorized in this scope)
        if isinstance(n, complex) or isinstance(n, float):
            return "Error: Factorial requires a positive integer, not complex or float."
        if n < 0:
            return "Error: Factorial is not defined for negative numbers."
        
        try:
            result = math.factorial(n)
            # Save to history
            equation = f"Factorial({n}) = {result}"
            self.history.append(equation)
            return result
        except Exception as e:
            return f"Error: {e}"

    def show_history(self):
        # Return the stored history list
        if not self.history:
            return ["No calculations in history yet."]
        return self.history


def display_menu():
    # Print the user interface menu to the console
    print("\n" + "="*30)
    print("Advanced OOP Calculator")
    print("="*30)
    print("1. Basic Math (+, -, *, /, %)")
    print("2. Factorial (!)")
    print("3. Show History")
    print("4. Exit")
    print("-" * 30)

def parse_input(user_input):
    # Helper function to convert string input to float or complex number
    try:
        if 'j' in user_input:
            return complex(user_input.replace(' ', ''))
        return float(user_input)
    except ValueError:
        return None

def main_workflow():
    # 1. Instantiate the object (Create the factory)
    calc = AdvancedCalculator() 
    
    # 2. Main execution loop
    while True:
        display_menu()
        choice = input("Enter your choice (1-4):").strip()
        
        if choice == '1':
            num1_str = input("Enter the first number (e.g., 5, 3.14, 2+3j): ")
            num1 = parse_input(num1_str)
            if num1 is None:
                print("Invalid number format!")
                continue
                
            op = input("Enter an operator (+, -, *, /, %): ").strip()
            
            num2_str = input("Enter the second number: ")
            num2 = parse_input(num2_str)
            if num2 is None:
                print("Invalid number format!")
                continue
                
            result = calc.perform_basic_math(num1, num2, op)
            print(f"\n Result: {result}")
            
        elif choice == '2':
            try:
                n = int(input("Enter a non-negative integer for factorial: ").strip())
                result = calc.perform_factorial(n)
                print(f"\n Result: {result}")
            except ValueError:
                print("Invalid input. Factorial requires an integer.")
                
        elif choice == '3':
            print("\n--- Calculation History ---")
            for record in calc.show_history():
                print(record)
                
        elif choice == '4':
            print("Exiting the calculator. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")


# Execution Trigger
if __name__ == "__main__":
    main_workflow()