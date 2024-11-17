import hashlib

from flask import session

from auth import generate_token
from database import db, UserDB
from exceptions import CustomException

def login(username, password):
    user = UserDB.query.filter_by(username=username).first()
    if not user:
        raise CustomException("User doesn't exist", 401)
    password = hashlib.md5(password.encode()).hexdigest()
    if user.password != password:
        raise CustomException("Password doesn't match", 401)
    token = generate_token(user)
    return token

def register(user:UserDB):
    existing_user = UserDB.query.filter_by(username=user.username).all()
    if existing_user:
        raise CustomException("Username already in use", 400)
    user.password = hashlib.md5(user.password.encode()).hexdigest()
    db.session.add(user)
    db.session.commit()

def change_password(username, old_password, new_password):
    user = UserDB.query.filter_by(username = username).first()
    if not user:
        raise CustomException("User does not exist", 400) 
    old_password = hashlib.md5(old_password.encode()).hexdigest()
    if user.password != old_password:
        raise CustomException("Password invalid", 401)
    new_password = hashlib.md5(new_password.encode()).hexdigest()
    user.password = new_password
    db.session.commit()