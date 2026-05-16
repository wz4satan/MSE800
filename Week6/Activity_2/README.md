# Zoo Application Login System

## Project Overview
This project is a simple, modular Zoo Application backend system designed to simulate an administrator's daily workflow. It implements a secure login authentication system and an animal status checking process using **Python Decorators**. 

The core objective of this project is to demonstrate how decorators can be used to control execution flow, manage user authentication, and cleanly separate security logic from core business functions.

## Project Structure
To maintain a clean architecture and adhere to the Single Responsibility Principle, the project is divided into three distinct modules:

* `decorators.py`: Contains the security and logging logic (the decorators). It handles user input, credential verification, and timestamp generation.
* `users_functions.py`: Contains the core business logic functions of the application (e.g., logging into the system, checking animal status).
* `main.py`: The entry point of the application. It acts as the central dispatcher, managing the data flow (user session) between different functions based on the authentication results.

## Functionality
1.  **Authentication Interception**: When the application runs, the system intercepts the execution and prompts the user to enter their Admin Name and Password.
2.  **Credential Validation**: The system checks the input against predefined authorized credentials (`ZheWang` / `abc12345678`).
3.  **Conditional Execution**: 
    * If credentials are correct: Grants access, logs the punch-in time, and proceeds to the workflow (checking animal status).
    * If credentials are wrong: Denies access, terminates the process, and prevents any further restricted operations.

## How the Decorators are Implemented
This project utilizes two custom decorators to enhance the core functions without modifying their internal code:

### 1. `@administor_log` (The Gatekeeper)
* **Implementation**: Placed directly above the `admin_login()` function. Inside its `wrapper`, it uses `input()` to collect user credentials before allowing the target function to execute.
* **Control Flow**: It uses an `if/else` statement. Only if the credentials match, it executes `func(*args, **kwargs)`. 
* **Data Passing (Session Simulation)**: Once authenticated, it `return input_username` back to `main.py`. This acts as a session token, passing the authenticated user's identity to subsequent functions that require authorization.

### 2. `@animals_info_manage` (The Logger)
* **Implementation**: Placed above the `check_animals_status(username)` function. 
* **Function**: It acts as an operational logger. Every time a user attempts to check the animals' status, this decorator automatically fetches the current system time using `datetime.now()` and prints a formatted timestamp before the core action is performed.

## How to Run
1. Ensure you have Python 3.x installed.
2. Clone or download this repository.
3. Open your terminal and navigate to the project directory.
4. Run the main script:
   ```bash
   python main.py