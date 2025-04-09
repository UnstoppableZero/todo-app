from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from storage import load_tasks, save_tasks

app = Flask(__name__)

app.secret_key = "your_secret_key"
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

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


@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        #Create a User
        new_user = User(username = username, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect("/login")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if the user exists in the database
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)  # Log the user in using Flask-Login

            flash("Login successful!", "success")
            return redirect("/dashboard")  # Redirect to the dashboard or home page

        flash("Login failed. Check your username or password.", "danger")

    return render_template("login.html")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique = True, nullable = False) #User's username
    password = db.Column(db.String(150), nullable = False) #User's password which is hashed

    def __repr__(self):
        return f'<User {self.username}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Task ID (primary key)
    task = db.Column(db.String(200), nullable=False)  # Task name
    due = db.Column(db.String(100), nullable=True)  # Task due date
    priority = db.Column(db.String(50), nullable=True)  # Task priority (Low, Medium, High)
    done = db.Column(db.Boolean, default=False)  # Task completion status
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key linking task to user
    user = db.relationship('User', back_populates='tasks')  # Relationship to the User model

User.tasks = db.relationship('Task', back_populates='user')  # Define relationship between User and Task

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



if __name__ == "__main__":
    app.run(debug=True)
