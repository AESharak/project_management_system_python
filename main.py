from userService import handle_register, handle_login, handle_logout
from projectService import handle_create_project, handle_view_project, handle_update_project, handle_delete_project
import app_state

def show_menu():
    print("\n=== Crowdfunding Console App ===")
    if app_state.current_user:
        print(f"Logged in as: {app_state.current_user.email}")
        print("1. Create Project")
        print("2. View My Projects")
        print("3. Update Project")
        print("4. Delete Project")
        print("5. Logout")
        print("6. Exit")
    else:
        print("1. Register")
        print("2. Login")
        print("3. Exit")

def main():
    while True:
        show_menu()
        choice = input("\nPick the number of the option you want to choose: ")
        
        if app_state.current_user:
            if choice == "1":
                handle_create_project()
            elif choice == "2":
                handle_view_project()
            elif choice == "3":
                handle_update_project()
            elif choice == "4":
                handle_delete_project()
            elif choice == "5":
                handle_logout()
            elif choice == "6":
                print("Thank you for using Crowdfunding Console App!")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            if choice == "1":
                handle_register()
            elif choice == "2":
                success = handle_login()
                if success:
                    print("\n=== Welcome to Project Management ===")
                    print("You now have access to project management features!")
            elif choice == "3":
                print("Thank you for using Crowdfunding Console App!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()