import datetime
import os
import csv

task_list = []


# Function for user login
def login():

    username = input("Enter username: ")
    password = input("Enter password: ")

    # Check if the entered username and password match any user in the "users.txt" file
    with open("users.txt", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2 and row[0] == username and row[1] == password:
                print("Login successful! Welcome " + username)
                return username, password

    print("Invalid username or password.")
    return None


# Function for user registration
def register():
    username = input("Enter a new username: ")

    with open("users.txt", "r") as file:
        for line in file:
            try:
                user, _ = line.strip().split(",")
                if user == username:
                    print("Username already exists. Please choose a different username.")
                    return
            except ValueError:
                continue

    password = input("Enter a new password: ")
    with open("users.txt", "a") as file:
        file.write(f"\n{username},{password}")

    print("Registration successful!")


# Function to add a new task
def add_task():
    task_username = input("Enter the username of the person the task is assigned to: ")
    task_title = input("Enter the title of the task: ")
    task_description = input("Enter the description of the task: ")
    task_due_date = input("Enter the due date of the task (eg. 21 Feb 2023): ")

    task_date_created = datetime.date.today().strftime("%d %B %Y")

    with open("tasks.txt", "r+") as f:
        lines = f.readlines()

        # Get the last task number
        if lines:
            last_line = lines[-1].strip()
            last_task_fields = last_line.split(", ")
            if len(last_task_fields) >= 1:
                last_task_number = int(last_task_fields[0])
                new_task_number = last_task_number + 1
            else:
                new_task_number = 1
        else:
            new_task_number = 1

        # Create the new task line
        new_task_line = f"\n{new_task_number}, {task_username}, {task_title}, {task_description}, {task_date_created}, {task_due_date}, No"
        # Append the new task line to the file
        f.write(new_task_line)

    print("Task added successfully!")


  
# Function to view all tasks
def view_all():
    with open("tasks.txt", "r") as file:
        tasks = file.readlines()

    if tasks:
        print("All Tasks:")
        print("-----------")

        for index, task in enumerate(tasks, start=1):
            task_data = task.strip().split(", ")
            task_number = index
            print("Task Number:", task_number)
            print("Title:", task_data[2])
            print("Assigned To:", task_data[1])
            print("Description:", task_data[3])
            print("Date Created:", task_data[3])
            print("Due Date:", task_data[4])
            print("Completed:", task_data[5])
            print("-----------------------")
    else:
        print("No tasks found.")


# Function to view tasks assigned to the logged-in user
def view_mine(username):
    
    with open("tasks.txt", "r") as file:
        tasks = file.readlines()

    if tasks:
        print("All Tasks:")
        print("-----------")
        
        for index, task in enumerate(tasks, start=1):
        
            task_data = task.strip().split(", ")
            
            if task_data[1] == logged_in_user[0]:
                
            
                task_number = index
                print("Task Number:", task_number)
                print("Title:", task_data[2])
                print("Assigned To:", task_data[1])
                print("Description:", task_data[3])
                print("Date Created:", task_data[4])
                print("Due Date:", task_data[5])
                print("Completed:", task_data[6])
                print("-----------------------")
    else:
        print("No tasks found.")


# Function to mark  task as complete
def mark_task_complete(task_num):
    
    with open("tasks.txt", "r") as file:
        task_lines = file.readlines()

    if task_num >= 1 and task_num <= len(task_lines):
        task_index = task_num - 1
        task = task_lines[task_index].strip().split(", ")

        if task[6] == "Yes":
            print("Task is already marked as complete.")
        else:
            task[6] = "Yes"
            task_lines[task_index] = ", ".join(task) + "\n"

            with open("tasks.txt", "w") as file:
                file.writelines(task_lines)

            print("Task marked as complete.")
    else:
        print("Invalid task number.")


# Function to edit a task
def edit_task(task_num):

    task_index = task_num - 1

    if task_index >= 0 and task_index < len(task_list):
        new_title = input("Enter the new title: ")
        new_description = input("Enter the new description: ")
        new_due_date = input("Enter the new due date (eg. 21 Feb 2023): ")
        task_list[task_index][1] = new_title
        task_list[task_index][2] = new_description
        
        print("Task updated successfully!")
    else:
        print("Invalid task number.")


# Function to generate task  overview report
def generate_task_overview():
    
    total_tasks = len(task_list)
    completed_tasks = 0
    uncompleted_tasks = 0
    overdue_tasks = 0

    for task in task_list:
        if task[6] == "Yes":
            completed_tasks += 1
        else:
            uncompleted_tasks += 1
            due_date = datetime.strptime(task[5], "%d %b %Y")
            if due_date < datetime.today():
                overdue_tasks += 1

    percentage_incomplete = (uncompleted_tasks / total_tasks) * 100
    percentage_overdue = (overdue_tasks / total_tasks) * 100

    with open("task_overview.txt", "w") as f:
        f.write(f"Total tasks: {total_tasks}\n")
        f.write(f"Completed tasks: {completed_tasks}\n")
        f.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        f.write(f"Overdue tasks: {overdue_tasks}\n")
        f.write(f"Percentage incomplete: {percentage_incomplete:.2f}%\n")
        f.write(f"Percentage overdue: {percentage_overdue:.2f}%\n")


# Function to generate user overview
def generate_user_overview():
    users = set()
    user_tasks = {}

    for task in task_list:
        users.add(task[1])
        if task[1] not in user_tasks:
            user_tasks[task[1]] = {
                'total_tasks': 0,
                'completed_tasks': 0,
                'uncompleted_tasks': 0,
                'overdue_tasks': 0
            }

        user_tasks[task[1]]['total_tasks'] += 1
        if task[6] == "Yes":
            user_tasks[task[1]]['completed_tasks'] += 1
        else:
            user_tasks[task[1]]['uncompleted_tasks'] += 1
            due_date = datetime.strptime(task[5], "%d %b %Y")
            if due_date < datetime.today():
                user_tasks[task[1]]['overdue_tasks'] += 1

    with open("user_overview.txt", "w") as f:
        f.write(f"Total users: {len(users)}\n")
        f.write("Users:\n")

        for user in users:
            tasks = user_tasks[user]
            total_tasks = tasks['total_tasks']
            completed_tasks = tasks['completed_tasks']
            uncompleted_tasks = tasks['uncompleted_tasks']
            overdue_tasks = tasks['overdue_tasks']

            percentage_total = (total_tasks / len(task_list)) * 100
            percentage_completed = (completed_tasks / total_tasks) * 100
            percentage_uncompleted = (uncompleted_tasks / total_tasks) * 100
            percentage_overdue = (overdue_tasks / total_tasks) * 100

            f.write(f"{user}\n")
            f.write(f"Total tasks assigned: {total_tasks}\n")
            f.write(f"Percentage of total tasks assigned: {percentage_total:.2f}%\n")
            f.write(f"Percentage of completed tasks: {percentage_completed:.2f}%\n")
            f.write(f"Percentage of tasks to be completed: {percentage_uncompleted:.2f}%\n")
            f.write(f"Percentage of overdue tasks: {percentage_overdue:.2f}%\n")
            f.write("\n")


# Main program
logged_in_user = None
while logged_in_user is None:
    logged_in_user = login()
    if logged_in_user is None:
        print("Please try again.\n")

# Read task data from file and populate task_list
with open("tasks.txt", "r") as f:
    for line in f:
        fields = line.strip().split(", ")
        task_list.append(fields)


if logged_in_user[0] == "admin":
    while True:
        # Admin menu options
        menu = input('''Select one of the following options below:
        r - Register a user
        a - Add a task
        va - View all tasks
        vm - View my tasks
        g - Generate statistics
        d - Display statistics
        e - Exit
        : ''').lower()

        if menu == 'r':
            register()


        elif menu == 'a':
           add_task()


        elif menu == 'va':
            view_all()


        elif menu == 'vm':
            view_mine(logged_in_user[0])


            task_num = input("Enter the task number to perform an action (or -1 to return to the main menu): ")
            if task_num == "-1":
                continue
            else:
                task_num = int(task_num)
                if task_num >= 1 and task_num <= len(task_list):
                    action = input("Select an action to perform on the task (m - mark as complete, e - edit task): ")
                    if action == "m":
                        mark_task_complete(task_num)
                    elif action == "e":
                        edit_task(task_num)
                    else:
                        print("Invalid action.")
                else:
                    print("Invalid task number.")

        elif menu == 'g':

            generate_task_overview()
            generate_user_overview()
            print("Statistics generated.")

        elif menu == 'd':
            with open("task_overview.txt", "r") as f:
                task_overview = f.read()
                print(task_overview)

            with open("user_overview.txt", "r") as f:
                user_overview = f.read()
                print(user_overview)

        elif menu == 'e':
            break

        else:
            print("Invalid input. Please try again.")

# User menu for logged-in users other than "admin"
else:
    while True:
        # User menu options
        menu = input('''Select one of the following options below:
        a - Add a task
        va - View all tasks
        vm - View my tasks
        e - Exit
        : ''').lower()

        if menu == 'a':
           add_task()

        elif menu == 'va':
            view_all()

        elif menu == 'vm':
            view_mine(logged_in_user[0])

            task_num = input("Enter the task number to perform an action (or -1 to return to the main menu): ")
            if task_num == "-1":
                continue
            else:
                task_num = int(task_num)
                if task_num >= 1 and task_num <= len(task_list):
                    action = input("Select an action to perform on the task (m - mark as complete, e - edit task): ")
                    if action == "m":
                        mark_task_complete(task_num)
                    elif action == "e":
                        edit_task(task_num)
                    else:
                        print("Invalid action.")
                else:
                    print("Invalid task number.")

        elif menu == 'e':
            break

        else:
            print("Invalid input. Please try again.")
