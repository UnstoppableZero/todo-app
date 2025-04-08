from ui import print_menu, display_tasks
from storage import load_tasks, save_tasks



def add_task(tasks):
     new_task_text = input("Enter new task: ")
     due_date = input("Enter due date (e.g. 2025-04-07): ")
     priority = input("Enter priority (Low, Medium, High): ").capitalize()
     new_task = {
        "task": new_task_text,
        "done": False,
        "due": due_date,
        "priority": priority
            }
     tasks.append(new_task)
     save_tasks(tasks)
     print("Task added!")


def mark_task_completed(tasks):
    if not tasks:
        print("No tasks to mark as completed.")
    else:
        for i, task in enumerate(tasks):
            status = "[x]" if task ["done"] else "[ ]"
            print(f"{i + 1}. {status} {task['task']}")
        try:
            task_num = int(input("Enter task number to mark as completed: "))
            if 1 <= task_num <= len(tasks):
                tasks[task_num - 1]["done"] = True
                save_tasks(tasks)
                print("Task marked as completed!")
            else:
                print("Invalid Task Number.")
        except ValueError:
                print("Please enter a valid number")

def clear_completed_tasks(tasks):
    tasks = [task for task in tasks if not task["done"]]
    save_tasks(tasks)
    print("Completed tasks have been cleared!")


def main():

    tasks = load_tasks()
   
    while True:
        print_menu()
        choice = input("Choose an option: ")

        if choice == '1':
            display_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            mark_task_completed(tasks)
        elif choice == '4':
            clear_completed_tasks(tasks)
        elif choice == '5':
            print("Bye")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
