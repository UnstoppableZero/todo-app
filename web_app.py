from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from storage import load_tasks, save_tasks

app = Flask(__name__)

#Configuring SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db' # SQLite database for users
app.config['SECRET_KEY'] = 'your-secret-key' # Secret key for session management
db = SQLAlchemy(app) # Initialize SQLAlchemy with the app

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)



@app.route("/add", methods = ["POST"])
def add_task():
    task_text = request.form["task"]
    due_date = request.form["due"]
    priority = request.form["priority"]

    new_task = {
        "task": task_text,
        "done": False,
        "due": due_date,
        "priority": priority
    }

    tasks = load_tasks()
    tasks.append(new_task)
    save_tasks(tasks)

    return redirect("/")


@app.route("/complete/<int:task_id>", methods = ["POST"])
def complete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = True
        save_tasks(tasks)
    return redirect("/")

@app.route("/delete/<int:task_id>", methods = ["POST"])
def delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect("/")


@app.route("/edit/<int:task_id>", methods = ["GET", "POST"])
def edit_task(task_id):
    tasks = load_tasks()
    if 0 <task_id < len(tasks):
        task = tasks[task_id]

        if request.method == "POST":
            #Update Task Data
            task["task"] = request.form["task"]
            task["due"] = request.form["due"]
            task["priority"] = request.form["priority"]
            save_tasks(tasks)
            return redirect("/")
        
        return render_template("edit_task.html", task = task, task_id = task_id)
    
    return redirect("/")

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True, nullable = False) #User's username
    password = db.Column(db.String(150), nullable = False) #User's password which is hashed

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Task ID (primary key)
    task = db.Column(db.String(200), nullable=False)  # Task name
    due = db.Column(db.String(100), nullable=True)  # Task due date
    priority = db.Column(db.String(50), nullable=True)  # Task priority (Low, Medium, High)
    done = db.Column(db.Boolean, default=False)  # Task completion status
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key linking task to user
    user = db.relationship('User', back_populates='tasks')  # Relationship to the User model

User.tasks = db.relationship('Task', back_populates='user')  # Define relationship between User and Task

if __name__ == "__main__":
    app.run(debug=True)
