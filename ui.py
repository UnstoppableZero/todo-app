def display_tasks(tasks):
    """Display the list of tasks."""
    for i, task in enumerate(tasks):
        status = "✅" if task["done"] else "⬜"
        due = task.get("due", "No due date")
        priority = task.get("priority", "No priority")

        print(f"{i + 1}. {status} {task['task']} — 📅 {due} - Priority: {priority}")

def print_menu():
    """Print the main menu."""
    print("\n📝 TODO LIST APP")
    print("---------------------")
    print("1️⃣  View tasks")
    print("2️⃣  Add task")
    print("3️⃣  Mark task as completed")
    print("4️⃣  Clear completed tasks")
    print("5️⃣  Exit\n")