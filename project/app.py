import os
import sqlite3

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for,jsonify
from flask_session import Session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")

def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def apology(message):
    """Render message as an apology to user."""
    return render_template("apology.html", message=message)

def apology1(message):
    """Render message as an apology to user."""
    message = request.args.get("message")
    return jsonify({"apology": message})

@app.route("/")
@login_required
def index():
    """Show all to do lists"""
    tasks_all = []
    lists = db.execute("SELECT * FROM lists WHERE user_id = :user_id",
                           user_id=session["user_id"])
    if lists:
        for list in lists:
            tasks = db.execute("SELECT * FROM tasks WHERE list_id = :list_id",list_id=list["id"])
            list_dict = {"title": list["title"], "color": list["color"], "id": list["id"]}
            if tasks:
                for i, task in enumerate(tasks):
                    list_dict[f"task{i}"] = task["task"]
            tasks_all.append(list_dict)

    return render_template("index.html", tasks_all=tasks_all)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Please provide username")

        elif not request.form.get("password"):
            return apology("Please provide password")

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("Invalid username and/or password")

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        username = request.form.get("username")
        if not username:
            return apology("Please enter a username")

        user_exists = db.execute(
            "SELECT * FROM users WHERE username = :username", username=username)
        if user_exists:
            return apology("Username is taken, please enter a valid username")

        password = request.form.get("password")
        if not password:
            return apology("Please enter a password")

        if len(password) < 6:
            return apology("Your password must have at least 6 caracters")

        password_confirmation = request.form.get("confirm-password")
        if password_confirmation != password:
            return apology("Your password confirmation does not match your password")

        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (hash, username) VALUES(?, ?)", hashed_password, username)
    else:
        return render_template('register.html')

    return redirect(url_for('login'))

@app.route("/create", methods=["GET", "POST"])
def create():
    """Create a new list"""
    if request.method == "GET":
        return render_template("create.html")

    if request.method == "POST":
        """Insert name of list, color, date, and user id into the lists table"""
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        data = request.get_json()
        title = data["title"].strip()
        color = request.get_json().get("color")

        db.execute("INSERT INTO lists (user_id, title, color, date) VALUES (:user_id, :title, :color, :date)",
           user_id=session["user_id"], title=title, color=color, date=date)
        return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    tasks_all = []
    list_rows = db.execute("SELECT * FROM lists WHERE user_id = ? AND id = ?", session["user_id"], id)
    if list_rows:
        list = list_rows[0]
        title = list['title']
        color = list['color']
        date = list['date']

    if request.method == "GET":
        tasks = db.execute("SELECT * FROM tasks WHERE list_id = ?", id)
        for task in tasks:
            tasks_all.append({
                'id': task['id'],
                'task': task['task'],
                'checkbox': task['checkbox']
            })

    if request.method == "POST":
        newtask = request.form.get("newtask")
        if newtask:
            db.execute("INSERT INTO tasks (list_id, task, checkbox) VALUES (?, ?, ?)", id, newtask, 0)
            tasks = db.execute("SELECT * FROM tasks WHERE list_id = ?", id)
            tasks_all = [{
                'id': task['id'],
                'task': task['task'],
                'checkbox': task['checkbox']
            } for task in tasks]

    return render_template("edit.html", tasks_all=tasks_all, title=title, color=color, date=date, id=id)


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    """Delete the list"""

    if request.method == "GET":
        return render_template("delete.html", id=id)

    if request.method == "POST":
        db.execute("DELETE FROM tasks WHERE list_id = :id", id=id)
        db.execute("DELETE FROM lists WHERE id = :id", id=id)

    return redirect("/")

@app.route("/change/<int:id>", methods=["GET", "POST"])
def change(id):
    """Change color of the list"""
    if request.method == "GET":
        return render_template("change.html", id=id)

    if request.method == "POST":
        """Update color of list in the lists table"""
        color = request.get_json().get("color")

        db.execute("UPDATE lists SET color= :color WHERE id= :id", id=id, color=color)
        return jsonify(success=True)

@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    completed = request.form.get('completed') == '1'
    list_id = request.form.get('list_id')
    db.execute("UPDATE tasks SET checkbox = ? WHERE id = ?", completed, task_id)
    return redirect(url_for('edit', id=list_id))

@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    """Delete the list"""

    if request.method == "POST":
        rows = db.execute("SELECT list_id FROM tasks WHERE id = :id", id=task_id)
        list_id = rows[0]['list_id']
        db.execute("DELETE FROM tasks WHERE id = :id", id=task_id)

    return redirect(url_for('edit', id=list_id))
