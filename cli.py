import requests
import os
import platform

BASE_URL = "http://127.0.0.1:5000/tasks"
SEARCH_BASE_URL = "http://127.0.0.1:5002/tasks/search"
EMAIL_BASE_URL = "http://127.0.0.1:5003/send_tasks_email"

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def print_menu():
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Edit Task")
    print("4. Set Language")
    print("5. Search Tasks")
    print("6. Send Tasks via Email")
    print("7. Export Tasks to .txt File")
    print("8. Exit")

def send_tasks_email():
    print("-----------------------------\n"
          "Sending tasks via email.\n"
          "-----------------------------")
    
    recipient = input("Enter recipient's email address: ")
    subject = input("Enter the subject line: ")
    
    payload = {
        'recipient': recipient,
        'subject': subject
    }
    
    try:
        response = requests.post(EMAIL_BASE_URL, json=payload)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except ValueError:
        print("Error decoding JSON from server response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    input("Press Enter to return to the menu...")

def export_tasks_to_txt():
    print("-----------------------------\n"
          "Exporting tasks to .txt file.\n"
          "-----------------------------")
    
    filename = input("Enter the filename to export to (e.g., tasks_export.txt): ")
    if not filename.endswith('.txt'):
        filename += '.txt'
    
    try:
        response = requests.get("http://127.0.0.1:5004/export", params={'filename': filename})
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except ValueError:
        print("Error decoding JSON from server response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    input("Press Enter to return to the menu...")


def search_tasks():
    print("-----------------------------\n"
          "Search for a task.\n"
          "-----------------------------")
    
    search_by_id = input("Search by ID? (y/n): ")
    if search_by_id.lower() == 'y':
        task_id = input("Enter task ID: ")
        response = requests.get(f"{SEARCH_BASE_URL}?id={task_id}")
    else:
        query = input("Enter search query (title or description): ")
        response = requests.get(f"{SEARCH_BASE_URL}?query={query}")
    
    try:
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        
        # Check if the response contains tasks or a message
        if 'tasks' in data:
            tasks = data.get('tasks', {})
            if not tasks:
                print("No tasks found.")
            else:
                for task_id, task in tasks.items():
                    title = task.get('title', 'No Title')
                    description = task.get('description', 'No Description')
                    print(f"ID: {task_id}, Title: {title}, Description: {description}")
        else:
            print("Error: Unexpected response structure")
    
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except ValueError:
        print("Error decoding JSON from server response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    input("Press Enter to return to the menu...")

def add_task():
    print("-----------------------\n"
          "Let's add another task!\n"
          "-----------------------")
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    task = {"title": title, "description": description}

    while True:
        choice = int(input("1. Save\n2. Cancel\n"))
        if choice == 1:
            try:
                response = requests.post(BASE_URL, json=task)
                response.raise_for_status()
                print(response.json())
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
            break
        elif choice == 2:
            clear_screen()
            return
        else:
            clear_screen()
            print("Please enter a valid choice.")
    clear_screen()

def remove_task():
    print("---------------------------------\n"
          "Finished up? Let's remove a task.\n"
          "---------------------------------")
    view_tasks()
    task_id = input("Enter task ID to remove: ")
    
    while True:
        try:
            choice = int(input(f"Are you sure you want to delete task {task_id}? \n1. Yes\n2. No\n"))
            if choice == 1:
                try:
                    response = requests.delete(f"{BASE_URL}/{task_id}")
                    response.raise_for_status()
                    print(response.json())
                except requests.exceptions.RequestException as e:
                    print(f"Error: {e}")
                clear_screen()
                break
            elif choice == 2:
                clear_screen()
                return
            else:
                clear_screen()
                print("Please enter a valid choice.")
        except ValueError:
            clear_screen()
            print("Please enter a number.")

def edit_task():
    print("-----------------------------\n"
          "Let's move some things around.\n"
          "-----------------------------")
    view_tasks()
    task_id = input("Enter task ID to edit: ")
    title = input("Enter new task title: ")
    description = input("Enter new task description: ")
    task = {"title": title, "description": description}
    while True:
        choice = int(input("Save changes?\n1. Yes\n2. No\n"))
        if choice == 1:
            try:
                response = requests.put(f"{BASE_URL}/{task_id}", json=task)
                response.raise_for_status()
                print(response.json())
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
            break
        elif choice == 2:
            clear_screen()
            return
        else:
            clear_screen()
            print("Please enter a valid choice.")
    clear_screen()

def view_tasks():
    response = requests.get(BASE_URL)
    try:
        data = response.json()
        tasks = data.get('tasks', {})
        
        if not tasks:
            print("You haven't got any tasks.")
        else:
            for task_id, task in tasks.items():
                # Check if 'title' and 'description' keys exist
                title = task.get('title', 'No Title')
                description = task.get('description', 'No Description')
                print(f"ID: {task_id}, Title: {title}, Description: {description}")
    except ValueError:
        print("Error decoding JSON from server response.")
    except KeyError as e:
        print(f"KeyError: Missing key {e}")

def set_language():
    print("-----------------------------\n"
          "Select a language:\n"
          "-----------------------------")
    languages = ["en", "es", "fr", "ar", "zh", "hi", "de", "ru", "it", "pt"]
    for i, lang in enumerate(languages, 1):
        print(f"{i}. {lang}")

    choice = int(input("Enter your choice: "))
    if 1 <= choice <= len(languages):
        selected_language = languages[choice - 1]
        response = requests.post("http://127.0.0.1:5000/language", json={'language': selected_language})
        print(response.json())
    else:
        print("Invalid choice. Please try again.")

def home_screen():
    clear_screen()
    print(
        "----------------------------------------------------\n"
        "Welcome to TaskFlow! Here's what we've got going on:\n"
        "----------------------------------------------------")
    view_tasks()
    print_menu()

def main():
    while True:
        home_screen()
        choice = input("Enter your choice: ")
        if choice == '1':
            clear_screen()
            add_task()
        elif choice == '2':
            clear_screen()
            remove_task()
        elif choice == '3':
            clear_screen()
            edit_task()
        elif choice == '4':
            clear_screen()
            set_language()
        elif choice == '5':
            clear_screen()
            search_tasks()
        elif choice == '6':
            clear_screen()
            send_tasks_email()
        elif choice == '7':
            clear_screen()
            export_tasks_to_txt()  # New functionality
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()