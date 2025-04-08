import json

import json

def load_tasks(filename="tasks.json"):
    """Load tasks from a JSON file."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist

def save_tasks(tasks, filename="tasks.json"):
    """Save tasks to a JSON file."""
    with open(filename, "w") as file:
        json.dump(tasks, file, indent=4)