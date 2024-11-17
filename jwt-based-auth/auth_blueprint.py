from flask import Blueprint, request, render_template, redirect

from database import db, UserDB
import db_ops
from exceptions import CustomException

bp = Blueprint("auth_blueprint", __name__)

@bp.route("/login", methods = ["POST"])
def login():
    try:
        data = request.get_json()
        username = data["username"].strip()
        username = username or None
        password = data["password"].strip()
        password = password or None
        if username is None or password is None:
            raise CustomException("Invalid body", 400)
        token = db_ops.login(username, password)
        return {"access_token": token}
    except CustomException as e:
        return e.response()
    except KeyError as e:
        return {"message": "Invalid body, missing "+str(e)}, 400
    except Exception as e:
        return {"message": "Exception "+str(e)}, 400

@bp.route("/register", methods = ["POST"])
def register():
    try:
        data = request.get_json()
        username = data["username"].strip()
        username = username or None
        password = data["password"].strip()
        password = password or None
        name = data["name"].strip()
        name = name or None
        phone = data.get("phone", "").strip()
        phone = phone or None
        age = data.get("age", None)
        if type(age) == str:
            age = age.strip()
            if not age:
                age = None
            elif age.isnumeric():
                age = int(age)
            else:
                raise CustomException("Age Invalid", 400)
        if username is None or password is None or name is None:
            raise CustomException("Invalid body", 400)
        user = UserDB(username, password, name, phone, age)
        db_ops.register(user)
        return {"message": "Successfully registered"}
    except CustomException as e:
        return e.response()
    except KeyError as e:
        return {"message": "Invalid body, missing "+str(e)}, 400
    except Exception as e:
        return {"message": "Exception "+str(e)}, 400
    

@bp.route("/update-password", methods = ["POST"])
def update_password():
    try:
        data = request.get_json()
        username = data["username"].strip()
        username = username or None
        old_password = data["old_password"].strip()
        old_password = old_password or None
        new_password = data["new_password"].strip()
        new_password = new_password or None
        if username is None or old_password is None or new_password is None:
            raise CustomException("Invalid body", 400)
        db_ops.change_password(username, old_password, new_password)
        return {"message": "Successfully password changed"}
    except CustomException as e:
        return e.response()
    except KeyError as e:
        return {"message": "Invalid body, missing "+str(e)}, 400
    except Exception as e:
        return {"message": "Exception "+str(e)}, 400
    

@bp.route("/logout", methods = ["GET"])
def logout():
    return redirect("/")