from class_Land import Land

def main():
    print("--- Land Dimension Calculator ---")
    
    try:
        # Get user input for dimensions
        user_length = float(input("Enter the length of the land: "))
        user_width = float(input("Enter the width of the land: "))

        # Instantiate the Land object
        my_land = Land(user_length, user_width)

        # Output the results using the class methods
        print("\n--- Property Details ---")
        my_land.print_dimensions()
        
        # Calculate and print area and perimeter
        area = my_land.calculate_area()
        perimeter = my_land.calculate_perimeter()
        
        print(f"Calculated Area: {area}")
        print(f"Calculated Perimeter: {perimeter}")

    except ValueError:
        print("Invalid input. Please enter numerical values for the dimensions.")

if __name__ == "__main__":
    main()