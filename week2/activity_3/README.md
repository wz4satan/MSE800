# Advanced OOP Calculator

## Project Description
This project is developed for Week 2 - Activity 3. It is a robust calculator that performs basic mathematical operations (+, -, *, /, %), factorial calculations, and fully supports both standard and complex numbers (e.g., `2+3j`).

## Alignment with Object-Oriented Programming (OOP) Concepts
To successfully transition from procedural programming to an Object-Oriented design, this project was structured based on the core principles of OOP:

1. **State & Attributes (Encapsulation)**: 
   The core logic is wrapped inside the `AdvancedCalculator` class. It utilizes the `__init__` method to initialize `self.history`, a state variable that stores the memory of past calculations. This ensures that the history is tied to the specific object instance rather than floating globally.

2. **Behaviors (Methods)**: 
   The calculator's capabilities are defined as methods (`perform_basic_math`, `perform_factorial`, `show_history`) within the class. They manipulate the internal state (`self.history`) and provide controlled access to the calculation engine, protecting the internal logic from external interference.

3. **Separation of Concerns**: 
   The project strictly separates the OOP business logic from the user interface. The class handles pure data manipulation, while stateless, independent functions (`display_menu()`, `parse_input()`, and `main_workflow()`) handle the console UI and control flow.

## Architecture Fulfilling the Requirements
* **Classes**: `AdvancedCalculator` (1 class)
* **Functions**: `display_menu()`, `parse_input()`, `main_workflow()` (3 independent functions)
* **Methods**: `__init__()`, `perform_basic_math()`, `perform_factorial()`, `show_history()` (4 methods)