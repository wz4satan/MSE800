# New Zealand Airline Flight System

This project is an Object-Oriented Programming (OOP) demonstration in Python, showcasing core software engineering concepts such as Classes, Inheritance, and Method Overriding. The project uses a New Zealand flight system as its business context.

## Project Structure

This project contains the following files:

* **`nz_airline_classes.py`**: The core logic module containing the flight data models.
  * `GeneralFlight`: The base (parent) class that defines common attributes shared by all flights (e.g., flight number, aircraft type, departure/arrival airports, departure time, and passenger count), as well as common methods like calculating the base fare.
  * `DomesticFlight`: The derived (child) class that inherits from `GeneralFlight`. It extends the base class with domestic-specific attributes (like `domestic_tax_rate`) and includes methods to calculate the final fare inclusive of tax.
* **`main.py`**: The main entry point and testing script. It demonstrates how to instantiate both general and domestic flight objects and calls their methods to display flight information and calculate fares.
* **`nz_airline_classes.jpg` / `nz_airline_classes.drawio`**: UML class diagram files. These provide a visual representation of the inheritance relationship and class structure between `GeneralFlight` and `DomesticFlight`.

## Key OOP Concepts Demonstrated

* **Inheritance**: The declaration `class DomesticFlight(GeneralFlight):` shows how a subclass directly inherits attributes and methods from a parent class. The subclass utilizes `super().__init__(...)` to call the parent's constructor, promoting code reusability.
* **Method Overriding**: `DomesticFlight` overrides the parent's `display_flight_info()` method. It uses `super().display_flight_info()` to execute the parent's print logic first, and then appends its own specific logic (printing the domestic tax rate), demonstrating method extension and polymorphism.

## How to Run

1. Ensure you have Python 3 installed on your macOS or system environment.
2. Place all the provided files in the same directory.
3. Open your terminal, navigate to the project directory, and execute the following command:

```bash
python main.py

```

## Expected to Output

Upon running the script, the console will output:

1. The general flight information and route (using the parent class instance).
2. The domestic flight information, including the specific domestic tax rate (using the child class instance).
3. A fare breakdown for a 350km flight distance, displaying both the Base Fare and the Final Fare (inclusive of the domestic tax).

