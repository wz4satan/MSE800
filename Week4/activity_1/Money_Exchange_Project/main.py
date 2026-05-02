from database import create_tables
from exchange_manager import add_customer, view_customers, delete_customer, add_branch, view_branches

def menu():
    print("\n==== Money Exchange Management System ====")
    print("1. Add Customer")
    print("2. View All Customers")
    print("3. Delete Customer by ID")
    print("4. Add New Branch")
    print("5. View All Branches")
    print("6. Exit")

def main():
    # 初始化数据库和表
    create_tables()
    
    while True:
        menu()
        choice = input("Select an option (1-6): ")
        
        if choice == '1':
            name = input("Enter customer name: ")
            email = input("Enter email: ")
            address = input("Enter address: ")
            phone = input("Enter phone number: ")
            add_customer(name, email, address, phone)
            
        elif choice == '2':
            customers = view_customers()
            print("\n--- Customer List ---")
            for customer in customers:
                print(customer)
                
        elif choice == '3':
            try:
                customer_id = int(input("Enter customer ID to delete: "))
                delete_customer(customer_id)
            except ValueError:
                print("❌ Please enter a valid numerical ID.")
                
        elif choice == '4':
            name = input("Enter branch name: ")
            status = input("Enter status (e.g., Active/Inactive): ")
            city = input("Enter city: ")
            location = input("Enter exact location: ")
            add_branch(name, status, city, location)
            
        elif choice == '5':
            branches = view_branches()
            print("\n--- Branch List ---")
            for branch in branches:
                print(branch)
                
        elif choice == '6':
            print("Goodbye! System exiting.")
            break
            
        else:
            print("❌ Invalid choice, try again.")

if __name__ == "__main__":
    main()