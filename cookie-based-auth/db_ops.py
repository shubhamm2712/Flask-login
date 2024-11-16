import hashlib

from flask import session

from database import db, UserDB

def login(username, password):
    user = UserDB.query.filter_by(username=username).first()
    if not user:
        return False, "Username doesn't exist"
    password = hashlib.md5(password.encode()).hexdigest()
    if user.password != password:
        return False, "Invalid Password"
    session["user"] = user.toJson()
    return True, "Successfully logged in"

def register(user:UserDB):
    existing_user = UserDB.query.filter_by(username=user.username).all()
    if existing_user:
        return False, "Username already exists"
    user.password = hashlib.md5(user.password.encode()).hexdigest()
    db.session.add(user)
    db.session.commit()
    return True, "Successfully Registered"

def change_password(username, old_password, new_password):
    user = UserDB.query.filter_by(username = username).first()
    if not user:
        return False, "User does not exist"
    old_password = hashlib.md5(old_password.encode()).hexdigest()
    if user.password != old_password:
        return False, "Invalid old password"
    new_password = hashlib.md5(new_password.encode()).hexdigest()
    user.password = new_password
    db.session.commit()
    return True, "Password Changed successfully"