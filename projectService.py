from Project import Project
import app_state
import json
import os
from datetime import datetime

projects = []

def load_projects():
    global projects
    if os.path.exists('projects.json'):
        try:
            with open('projects.json', 'r') as f:
                projects_data = json.load(f)
                # Note: We'll need to reconstruct the owner reference when loading
                projects = []
                for project_data in projects_data:
                    from userService import users
                    # Find the owner by email
                    owner_email = project_data.get('owner')
                    owner = None
                    for user in users:
                        if user.email == owner_email:
                            owner = user
                            break
                    
                    project = Project(
                        title=project_data['title'],
                        details=project_data['details'],
                        total_target=project_data['total_target'],
                        start_date=project_data['start_date'],
                        end_date=project_data['end_date'],
                        owner=owner  # Set the owner reference
                    )
                    project.current_amount = project_data['current_amount']
                    
                    # Handle created_at
                    if 'created_at' in project_data:
                        try:
                            project.created_at = datetime.fromisoformat(project_data['created_at'])
                        except ValueError:
                            project.created_at = datetime.now()
                    
                    projects.append(project)
                    
                    # Add the project to the owner's projects list if owner exists
                    if owner:
                        if not hasattr(owner, 'projects'):
                            owner.projects = []
                        if project not in owner.projects:
                            owner.projects.append(project)
        except Exception as e:
            print(f"Warning: Error loading projects: {e}")
            projects = []

def save_projects():
    with open('projects.json', 'w') as f:
        projects_data = [project.to_dict() for project in projects]
        json.dump(projects_data, f, indent=4)

def handle_create_project():
    if not app_state.current_user:
        print("Please login first!")
        return
    
    print("\n=== Create Project ===")
    title = input("Enter project title: ")
    details = input("Enter project details: ")
    
    try:
        total_target = float(input("Enter total target amount (EGP): "))
        if total_target <= 0:
            print("Target amount must be positive!")
            return
    except ValueError:
        print("Invalid amount!")
        return
    
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    
    if not Project.validate_dates(start_date, end_date):
        print("Invalid dates! Start date must be in the future and before end date.")
        return
    
    new_project = Project(title, details, total_target, start_date, end_date, app_state.current_user)
    projects.append(new_project)
    app_state.current_user.projects.append(new_project)
    save_projects()
    print("Project created successfully!")

def handle_view_project():
    if not app_state.current_user:
        print("Please login first!")
        return
    
    print("\n=== View Projects ===")
    
    # Filter projects to only show those owned by the current user
    user_projects = [p for p in projects if p.owner and p.owner.email == app_state.current_user.email]
    
    if not user_projects:
        print("You haven't created any projects yet.")
        return
    
    for i, project in enumerate(user_projects, 1):
        print(f"\nProject {i}:")
        print(f"Title: {project.title}")
        print(f"Details: {project.details}")
        print(f"Target: {project.total_target} EGP")
        print(f"Current Amount: {project.current_amount} EGP")
        print(f"Start Date: {project.start_date}")
        print(f"End Date: {project.end_date}")
        print(f"Owner: {project.owner.email}")

def handle_update_project():
    if not app_state.current_user:
        print("Please login first!")
        return
    
    print("\n=== Update Project ===")
    user_projects = [p for p in projects if p.owner == app_state.current_user]
    
    if not user_projects:
        print("You have no projects to update.")
        return
    
    print("\nYour Projects:")
    for i, project in enumerate(user_projects, 1):
        print(f"{i}. {project.title}")
    
    try:
        choice = int(input("\nSelect project number to update: ")) - 1
        if choice < 0 or choice >= len(user_projects):
            print("Invalid project number!")
            return
        
        project = user_projects[choice]
        print("\nLeave blank to keep current values:")
        
        title = input(f"New title [{project.title}]: ") or project.title
        details = input(f"New details [{project.details}]: ") or project.details
        
        total_target = input(f"New target [{project.total_target}]: ")
        total_target = float(total_target) if total_target else project.total_target
        
        start_date = input(f"New start date [{project.start_date}]: ") or project.start_date
        end_date = input(f"New end date [{project.end_date}]: ") or project.end_date
        
        if not Project.validate_dates(start_date, end_date):
            print("Invalid dates! Start date must be in the future and before end date.")
            return
        
        project.title = title
        project.details = details
        project.total_target = total_target
        project.start_date = start_date
        project.end_date = end_date
        
        save_projects()
        print("Project updated successfully!")
        
    except ValueError:
        print("Invalid input!")

def handle_delete_project():
    if not app_state.current_user:
        print("Please login first!")
        return
    
    print("\n=== Delete Project ===")
    user_projects = [p for p in projects if p.owner == app_state.current_user]
    
    if not user_projects:
        print("You have no projects to delete.")
        return
    
    print("\nYour Projects:")
    for i, project in enumerate(user_projects, 1):
        print(f"{i}. {project.title}")
    
    try:
        choice = int(input("\nSelect project number to delete: ")) - 1
        if choice < 0 or choice >= len(user_projects):
            print("Invalid project number!")
            return
        
        project = user_projects[choice]
        confirm = input(f"Are you sure you want to delete '{project.title}'? (y/n): ")
        
        if confirm.lower() == 'y':
            projects.remove(project)
            app_state.current_user.projects.remove(project)
            save_projects()
            print("Project deleted successfully!")
        else:
            print("Deletion cancelled.")
            
    except ValueError:
        print("Invalid input!")

# Initialize projects on module load
load_projects()