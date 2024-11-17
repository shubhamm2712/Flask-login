import hashlib

from flask import session
from sqlalchemy import select

from auth import generate_token
from database import db, UserDB
from exceptions import CustomException

def login(username, password):
    stmt = select(UserDB).where(UserDB.username == username)
    row = db.session.execute(stmt).one_or_none()
    if not row:
        raise CustomException("User doesn't exist", 401)
    user = row[0]
    password = hashlib.md5(password.encode()).hexdigest()
    if user.password != password:
        raise CustomException("Password doesn't match", 401)
    token = generate_token(user)
    return token

def register(user:UserDB):
    stmt = select(UserDB).where(UserDB.username == user.username)
    row = db.session.execute(stmt).one_or_none()
    if row:
        raise CustomException("Username already in use", 400)
    user.password = hashlib.md5(user.password.encode()).hexdigest()
    db.session.add(user)
    db.session.commit()

def change_password(username, old_password, new_password):
    stmt = select(UserDB).where(UserDB.username == username)
    row = db.session.execute(stmt).one_or_none()
    if not row:
        raise CustomException("User does not exist", 400) 
    user = row[0]
    old_password = hashlib.md5(old_password.encode()).hexdigest()
    if user.password != old_password:
        raise CustomException("Password invalid", 401)
    new_password = hashlib.md5(new_password.encode()).hexdigest()
    user.password = new_password
    db.session.commit()