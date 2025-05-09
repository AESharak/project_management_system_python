from User import User
import json
import os
from datetime import datetime
import app_state

# Global variables
users = []

def load_users():
    global users
    users = []  # Initialize empty users list
    if os.path.exists('users.json'):
        try:
            with open('users.json', 'r') as f:
                users_data = json.load(f)
                for user_data in users_data:
                    try:
                        # Create user without is_active and created_at
                        user = User(
                            first_name=user_data['first_name'],
                            last_name=user_data['last_name'],
                            email=user_data['email'],
                            password=user_data['password'],
                            mobile_phone=user_data['mobile_phone']
                        )
                        # Set additional attributes after creation
                        user.is_active = user_data['is_active']
                        
                        # Parse the created_at string to datetime object if it's a string
                        if isinstance(user_data['created_at'], str):
                            user.created_at = datetime.fromisoformat(user_data['created_at'])
                        else:
                            user.created_at = datetime.now()
                            
                        users.append(user)
                    except KeyError as e:
                        print(f"Warning: Skipping invalid user data - missing field: {e}")
                        continue
                    except ValueError as e:
                        print(f"Warning: Issue with user data format: {e}")
                        continue
        except json.JSONDecodeError:
            print("Warning: users.json is invalid, starting with empty users list")
            users = []

def save_users():
    try:
        with open('users.json', 'w') as f:
            users_data = [user.to_dict() for user in users]
            json.dump(users_data, f, indent=4)
    except Exception as e:
        print(f"Error saving users: {e}")

def handle_register():
    print("\n=== Registration ===")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    
    if not User.validate_email(email):
        print("Invalid email format!")
        return
    
    if any(user.email == email for user in users):
        print("Email already registered!")
        return
    
    password = input("Enter password (min 8 characters): ")
    if not User.validate_password(password):
        print("Password must be at least 8 characters long!")
        return
    
    confirm_password = input("Confirm password: ")
    if password != confirm_password:
        print("Passwords do not match!")
        return
    
    mobile_phone = input("Enter mobile phone (Egyptian format): ")
    if not User.validate_egyptian_phone(mobile_phone):
        print("Invalid Egyptian phone number format!")
        return
    
    new_user = User(first_name, last_name, email, password, mobile_phone)
    new_user.is_active = True
    users.append(new_user)
    save_users()
    print("Registration successful!")

def handle_login():
    print("\n=== Login ===")
    email = input("Enter email: ")
    password = input("Enter password: ")
    
    for user in users:
        if user.email == email and user.password == password:
            if not user.is_active:
                print("Account is not active!")
                return False
            app_state.current_user = user
            print(f"Welcome back, {user.first_name}!")
            return True
    
    print("Invalid email or password!")
    return False

def handle_logout():
    if app_state.current_user:
        print(f"Goodbye, {app_state.current_user.first_name}!")
        app_state.current_user = None
    else:
        print("No user is currently logged in!")

# Initialize users on module load
load_users()