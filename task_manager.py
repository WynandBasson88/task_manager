# Import the datetime module
import datetime

# Import the os.path module
import os.path

# Ask the user to enter their login details
def login():

    # Create a global variable user_name to be called from outside this function
    global user_name
    
    # Ask the user to enter his/her username and password
    user_name = input("Please enter your username and press enter: ")
    user_password = input("Please enter your password and press enter: ")

    # Call the the function user_dictionary() and save the return value in user_dict
    user_dict = user_dictionary()
    
    # Determine if the username and password entered matches one of the usernames and passwords in the text file "user.txt"
    for key in user_dict:
        if (user_name == user_dict[key]["username"] and user_password == user_dict[key]["password"]):
            menu_selection()

    # If the username and password entered do not match one of the usernames and passwords in the text file "user.txt" print an error message      
    print("\nThe username and password entered is not listed or correct. Please try again.\n")
    # Call the login() function again
    login()
    
# Display the options menu if the user successfully logs in
def menu():
    print("\nYou are successfully logged in as {}.\n".format(user_name))
    print("Please select one of the following options:")
    print("r - register user")
    print("a - add task")
    print("va - view all tasks")
    print("vm - view my tasks")
    print("e - exit")
    # Display these options only if user is admin
    if (user_name == "admin"):
        print("ds - display statistics")
        print("gr - generate reports")
        
    user_selection = input("\nSelect an option: ")
    print(" ")
    return user_selection

# Create a return menu to be called when other functions are finished executing
def return_menu():
    choice = input("Would you like to return to the selection menu? (Yes/No): ")
    choice = choice.lower()
    while (choice != "no" and choice != "yes"):
        print("You did not make a valid selection!")
        choice = input("Try again. Would you like to return to the selection menu? (Yes/No): ")
        choice = choice.lower()
    if (choice == "no"):
        print("You will now be logged out!")
        exit()
    if (choice == "yes"):
        menu_selection()

# Create a menu selection function that checks the user input and determines program flow
def menu_selection():
    user_choice = ""

    # Create a looping/running menu
    while(user_choice != "e"):
        user_choice = menu()
        
        # If an unexpected input is made continually ask the user to make a valid selection
        while (user_choice != "r" and user_choice != "a" and user_choice != "va" and user_choice != "vm" and user_choice != "e" and user_choice != "ds" and user_choice != "gr"):
            user_choice = invalid_entry()

        # If this selection is made by any user other than admin print an appropriate error message
        if (user_choice == "r" and user_name != "admin"):
            not_admin()

        #If this selection is made by admin allow admin to add a new user to the system
        if (user_choice == "r" and user_name == "admin"):
            reg_user()
            
        # If this selection is made ask the user to input all the relevant information about a specific task that needs to be added to text file "tasks.txt"
        if (user_choice == "a"):
            add_task()

        # If this selection is made display all the tasks that have been added to text file "tasks.txt"
        if (user_choice == "va"):
            view_all()

        # If this selection is made display all the tasks that the logged in user has to complete
        if (user_choice == "vm"):
            view_mine()

        # If any user other than admin makes this selection display an appropriate error message that tells them they do not have admin rights
        if (user_choice == "ds" and user_name != "admin"):
            access_denied()

        # If this selection is made and the user is admin display the total amount of users and tasks added to the text files "user.txt" and "tasks.txt"
        if (user_choice == "ds" and user_name == "admin"):
            display_stats()

        # If any user other than admin makes this selection display an appropriate error message that tells them they do not have admin rights
        if (user_choice == "gr" and user_name != "admin"):
            access_denied()

        # If this selection is made and the user is admin generate the reports user_overview and task_overview
        if (user_choice == "gr" and user_name == "admin"):
            generate_reports()

        # If the user makes this selection give the user the option to exit the program
        if (user_choice == "e"):
            exit()

# Display an appropriate error message if the user makes an invalid selection
def invalid_entry():
    print("You did not select a valid option. Try again.")
    user_selection = input("\nSelect an option (r, a, va, vm, e): ")
    print(" ")
    return user_selection

# Display an appropriate error message if the user is not logged in as admin and makes this selection "r"
def not_admin():
    print("A user cannot be added! User {} does not have admin rights.".format(user_name))

# Allow the user admin to register a new user when this selection is made "r" 
def reg_user():
    new_user = input("To register a new user please enter their username: ")
    
    # Create a dictionary where the username is the key and the password is the value
    user_file1 = open("user.txt", "r")
    name_password_dict = {}
    for line in user_file1:
        name_password_list = line.strip("\n").split(", ")
        name_password_dict[name_password_list[0]] = name_password_list[1]
    user_file1.close()

    # Check if the username already exists
    while (new_user in name_password_dict):
        print("This username already exists. Please try again!")
        new_user = input("To register a new user please enter their username or type exit to cancel: ")
        if(new_user == "exit"):
            exit()
        
    new_password = input("To register a new user please enter their password: ")
    confirm_password = input("Please confirm the password entered: ")

    # Check if the password entered was confirmed exactly
    while (confirm_password != new_password):
        print("The passwords entered did not match! Try again or type exit to cancel.")
        confirm_password = input("Please confirm the password entered or type exit: ")
        if (confirm_password == "exit"):
            exit()

    # Add the user to the file user.txt if the passwords entered matches
    if (confirm_password == new_password):
        user_file2 = open("user.txt", "a")
        user_file2.write("\n{}, {}".format(new_user, new_password))
        user_file2.close()
        print("User added!")

# Add a new task to the tasks.txt file when this selection is made "a"
def add_task():
    # Ask the user to enter the relevant information about the task
    user_assigned = input("Please enter the username of the person the task should be assigned to: ")
    task_title = input("Please enter the title of the task: ")
    task_description = input("Please enter a discription of the task: ")
    due_date = input("Please enter the date that the task should be completed (format: 20 Jan 2020): ")
    current_date = datetime.datetime.today()
    current_date = current_date.strftime("%d %b %Y")
    completed = "No"

    # Write the saved info about the task to a file tasks.txt
    task_file1 = open("tasks.txt", "a")
    task_file1.write("\n{}, {}, {}, {}, {}, {}".format(user_assigned, task_title, task_description, due_date, current_date, completed))
    task_file1.close()
    print("Task added successfully!")

# Display all the tasks in an oganised manner when this selection is made "va"
def view_all():
    # Call the task_dictionary() function and access data from it to be presented as information 
    print("The task list for all users is displayed below:\n")
    tasks = task_dictionary()
    for key in tasks:
        print("Task Number:\t\t{}".format(key))
        print("Assigned to:\t\t{}".format(tasks[key]["responsible"]))
        print("Task:\t\t\t{}".format(tasks[key]["task"]))
        print("Task Description:\t{}".format(tasks[key]["description"]))
        print("Due date:\t\t{}".format(tasks[key]["date_complete"]))
        print("Today's date:\t\t{}".format(tasks[key]["date_current"]))
        print("Task completed:\t\t{}".format(tasks[key]["completed"]))
        print("")

# Display all the tasks belonging to the user that is logged in in an organised manner when this selection is made "vm"
def view_mine():
    # Call the task_dictionary() function and access data from it to be presented as information
    user_found = False
    user_task_numbers = []
    print("The task list for user {} is displayed below:\n".format(user_name))
    tasks = task_dictionary()
    for key in tasks:
        if (user_name == tasks[key]["responsible"]):
            print("Task Number:\t\t{}".format(key))
            print("Task:\t\t\t{}".format(tasks[key]["task"]))
            print("Task Description:\t{}".format(tasks[key]["description"]))
            print("Due date:\t\t{}".format(tasks[key]["date_complete"]))
            print("Today's date:\t\t{}".format(tasks[key]["date_current"]))
            print("Task completed:\t\t{}".format(tasks[key]["completed"]))
            print("")
            user_found = True
            user_task_numbers.append(str(key))

    # If the boolean didn't toggle to True it means no tasks were found for the logged user and an appropriate message will be displayed
    if (user_found == False):
        print("No tasks were found for user {}!".format(user_name))
        return_menu()

    # Create functionality to edit a selected task by calling the edit_task() function
    edit_choice = input("Please select a task you would like to edit by entering the task number. Alternatively enter -1 to return to the selection menu: ")
    while (edit_choice != "-1" and edit_choice not in user_task_numbers):
        print("You did not enter a task number that belongs to you!")
        edit_choice = input("Try again or enter -1 to return to the selection menu: ")   
    if (edit_choice != "-1" and edit_choice in user_task_numbers):
        edit_choice = int(edit_choice)
        edit_task(edit_choice)  
    if (edit_choice == "-1"):
        menu_selection()

# A function that lets the user either mark a task as complete or allow the user to edit the due date or person responsible for the task   
def edit_task(choice):
    tasks = task_dictionary()

    # Display an options menu for editing the selected task
    print("\nPlease select one of the following options: ")
    print("1 - Mark the task as complete")
    print("2 - Edit the task")
    print("3 - Return to the main menu")
    selection = input("Select an option (1 - 3): ")
    print("")

    while (selection != "1" and selection != "2" and selection != "3"):
        print("You did not make a valid selection!")
        selection = input("Select an option (1 - 3): ")

    # If this selection is made the task will be marked as completed if not already marked
    if (selection == "1"):
        if (tasks[choice]["completed"] == "Yes"):
            print("The task has already been marked as complete!")
        elif (tasks[choice]["completed"] == "No"):
            tasks[choice]["completed"] = "Yes"
            print("Task {} has now been marked as complete!".format(choice))

    # If this selection is made and the task is not yet marked as complete a second selection menu will be displayed           
    elif (selection == "2"):
        if (tasks[choice]["completed"] == "Yes"):
            print("The task has already been marked as complete and therefor cannot be edited!")
            return_menu()
        print("\nPlease select one of the following options: ")
        print("1 - Edit the user that task {} is assigned to".format(choice))
        print("2 - Edit the due date of task {}".format(choice))
        print("3 - Return to the main menu")
        option = input("Select an option (1 - 3): ")
        print("")

        while (option != "1" and option != "2" and option != "3"):
            print("You did not make a valid selection!")
            option = input("Select an option (1 - 3): ")

        # If this selection is made change the user responsible for the task
        if (option == "1"):
            user_assigned = input("Please enter the username of the person the task should be assigned to: ")
            tasks[choice]["responsible"] = user_assigned

        # If this selection is made change the due date of the task
        elif (option == "2"):
            due_date = input("Please enter the due date that the task should be completed (format: 20 Dec 2020): ")
            tasks[choice]["date_complete"] = due_date

        # Call the return_menu() function if this selection is made
        elif (option == "3"):
            return_menu()

    # Call the return_menu() function if this selection is made
    elif (selection == "3"):
        return_menu()

    # Overwrite the text file tasks.txt with the new data    
    file = open("tasks.txt", "w")
    for key in tasks:
        file.write("{}, {}, {}, {}, {}, {}\n".format(tasks[key]["responsible"], tasks[key]["task"], tasks[key]["description"], tasks[key]["date_complete"], tasks[key]["date_current"], tasks[key]["completed"]))
    file.close()    

# Display an appropriate error message when this selection is made and the user is not admin "s"
def access_denied():
    print("This option is not available! User {} does not have admin rights.".format(user_name))

# Display the amount of registered users and tasks in user.txt and tasks.txt respectively
def display_stats():
    if not os.path.exists("task_overview.txt") and not os.path.exists("user_overview.txt"):
        generate_reports()

    # Open the task_overview.txt and user_overview.txt files and display the information in an organised manner   
    task_file = open("task_overview.txt", "r")
    task_information = task_file.read()
    task_file.close()
    print("TASK OVERVIEW")
    print(task_information)

    user_file = open("user_overview.txt", "r")
    user_information = user_file.read()
    task_file.close()
    print("USER OVERVIEW")
    print(user_information)

# Create a user dictionary from the text file user.txt
def user_dictionary():
    user_list = []
    user_dict = {}

    # Create a dictionary of dictionaries to be called in other functions
    user_file = open("user.txt", "r")
    for num, line in enumerate(user_file):
        user_list = line.strip("\n").split(", ")
        user_dict[num + 1] = {"username": user_list[0], "password": user_list[1]}
    user_file.close()
    return user_dict

# Create a task dictionary from the text file tasks.txt
def task_dictionary():
    task_list = []
    task_dict = {}

    # Create a dictionary of dictionaries to be called in other functions
    task_file = open("tasks.txt", "r")
    for num, line in enumerate(task_file):
        task_list = line.strip("\n").split(", ")
        task_dict[num + 1] = {"responsible": task_list[0], "task": task_list[1], "description": task_list[2], "date_complete": task_list[3], "date_current": task_list[4], "completed": task_list[5]}  
    task_file.close()
    return task_dict

# Create a function generate_reports that calls the functions task_overview() and user_overview() 
def generate_reports():
    task_overview()
    user_overview()
    print("The reports have been successfully generated!")
    print(" ")
    #return_menu()

# Create the function task_overview()
def task_overview():
    tasks_number = 0
    tasks_completed = 0
    tasks_uncompleted = 0
    tasks_overdue = 0
    percentage_uncompleted = 0.0
    percentage_overdue = 0.0

    task_dict = task_dictionary()

    # Create a for loop to loop through the task dictionary and increment variables based on the data in the dictionary
    for key in task_dict:
        tasks_number += 1

        if (task_dict[key]["completed"] == "Yes"):
            tasks_completed += 1
        elif (task_dict[key]["completed"] == "No"):
            tasks_uncompleted += 1

        # Create a datetime object from the string value stored at the key date_complete
        datetime_object = datetime.datetime.strptime(task_dict[key]["date_complete"], "%d %b %Y")
        if (datetime_object < datetime.datetime.today() and task_dict[key]["completed"] == "No"):
            tasks_overdue += 1

    # Create and write the data to a new text file task_overview.txt to be presented as information
    overview_file = open("task_overview.txt", "w")
    overview_file.write("The total number of tasks that have been created in the task manager: {}\n".format(tasks_number))
    overview_file.write("The total number of tasks completed: {}\n".format(tasks_completed))
    overview_file.write("The total number of tasks uncompleted: {}\n".format(tasks_uncompleted))
    overview_file.write("The total number of tasks overdue that haven't been completed: {}\n".format(tasks_overdue))
    if (tasks_number != 0): # Ensure you never divide by 0
        percentage_uncompleted = (tasks_uncompleted / tasks_number) * 100
        percentage_overdue = (tasks_overdue / tasks_number) * 100
        overview_file.write("The percentage of tasks that haven't been completed: {}%\n".format(round(percentage_uncompleted, 2)))
        overview_file.write("The percentage of tasks overdue: {}%\n".format(round(percentage_overdue, 2)))
    overview_file.close()

# Create a function user_overview()    
def user_overview():
    tasks_number = 0
    users_number = 0

    task_dict = task_dictionary()
    user_dict = user_dictionary()

    # Create and write the data to a new text file user_overview.txt to be presented as information
    overview_file = open("user_overview.txt", "w")
    
    for key in task_dict:
        tasks_number +=1

    for key in user_dict:
        users_number += 1

    # Create and write the data to a new text file user_overview.txt to be presented as information
    overview_file.write("The total number of tasks that have been created in the task manager: {}\n".format(tasks_number))  
    overview_file.write("The total number of users registered with the task manager: {}\n\n".format(users_number)) 

    # Create a nested for loop to loop through the user dictionary and task dictionary and increment variables based on the data in the dictionaries 
    for user in user_dict:
        tasks_num_user = 0
        tasks_completed = 0
        tasks_uncompleted = 0
        tasks_overdue = 0
        percent_tasks_user = 0.0
        percent_user_completed = 0.0
        percent_user_uncompleted = 0.0
        percent_uncomplete_overdue = 0.0

        for task in task_dict:
            if(user_dict[user]["username"] == task_dict[task]["responsible"]):
                tasks_num_user += 1
                if (task_dict[task]["completed"] == "Yes"):
                    tasks_completed += 1
                if (task_dict[task]["completed"] == "No"):
                    tasks_uncompleted += 1

                # Create a datetime object from the string value stored at the key date_complete
                datetime_object = datetime.datetime.strptime(task_dict[task]["date_complete"], "%d %b %Y")
                if (task_dict[task]["completed"] == "No" and datetime_object < datetime.datetime.today()):
                    tasks_overdue += 1

        # Create and write the data to a new text file user_overview.txt to be presented as information  
        overview_file.write("User {} is responsible for {} tasks out of {}\n".format(user_dict[user]["username"], tasks_num_user, tasks_number))
        
        if (tasks_number != 0): # Ensure you never divide by 0
            percent_tasks_user = (tasks_num_user/tasks_number) * 100
            overview_file.write("User {} has been assigned {}% of the workload (of the {} tasks)\n".format(user_dict[user]["username"], round(percent_tasks_user, 2), tasks_number))

        overview_file.write("User {} has completed {} tasks out of the {}\n".format(user_dict[user]["username"], tasks_completed, tasks_num_user))
            
        if (tasks_num_user != 0): # Ensure you never divide by 0
            percent_user_completed = (tasks_completed/tasks_num_user) * 100 
            overview_file.write("User {} has completed {}% of the {} tasks\n".format(user_dict[user]["username"], round(percent_user_completed), tasks_num_user))

            percent_user_uncompleted = (tasks_uncompleted/tasks_num_user) * 100
            overview_file.write("User {} has not completed {}% of the {} tasks\n".format(user_dict[user]["username"], round(percent_user_uncompleted), tasks_num_user))

            percent_uncomplete_overdue = (tasks_overdue/tasks_num_user) * 100
            overview_file.write("User {} has {}% tasks uncompleted and overdue\n".format(user_dict[user]["username"], round(percent_uncomplete_overdue)))

        overview_file.write("User {} has {} tasks uncompleted and overdue\n".format(user_dict[user]["username"], tasks_overdue))
        
        overview_file.write("\n")  

    # Close the file
    overview_file.close()
    
    
# Call the login() function
login()






