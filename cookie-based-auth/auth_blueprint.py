from flask import Blueprint, request, render_template, redirect, flash, session

from database import db, UserDB
import db_ops

bp = Blueprint("auth_blueprint", __name__)

@bp.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        if username is None or password is None:
            return {"error":"Username or password is None"}, 400
        status, msg = db_ops.login(username, password)
        if status:
            flash(msg)
            return redirect('/')
        flash(msg)
    return render_template("login.html")

@bp.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", None)
        password = request.form.get("password", None)
        name = request.form.get("name", None)
        phone = request.form.get("phone", None)
        age = request.form.get("age", None)
        if age.isnumeric():
            age = int(age)
        else:
            age = None
        if username is None or password is None or name is None:
            return {"error":"Username, password or name is None"}, 400
        user = UserDB(username, password, name, phone, age)
        status, msg = db_ops.register(user)
        if status:
            flash(msg)
            return redirect("/")
        flash(msg)
    return render_template("register.html")

@bp.route("/update-password", methods = ["GET","POST"])
def update_password():
    if request.method == "POST":
        username = request.form.get("username", None)
        old_password = request.form.get("old_password", None)
        new_password = request.form.get("new_password", None)
        status, msg = db_ops.change_password(username, old_password, new_password)
        flash(msg)
        if status:
            return redirect("/")
    return render_template("update_password.html")

@bp.route("/logout")
def logout():
    if "user" in session:
        session.pop("user")
        flash("Logged out")
    return redirect("/")