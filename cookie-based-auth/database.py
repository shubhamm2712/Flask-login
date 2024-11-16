from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserDB(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username: str = db.Column(db.String(80), unique = True, nullable = False)
    password: str = db.Column(db.String(120), nullable = False)
    name: str = db.Column(db.String(30), nullable = False)
    phone = db.Column(db.String(15))
    age = db.Column(db.Integer)

    def __init__(self, username, password, name, phone = None, age = None):
        self.username = username
        self.password = password
        self.name = name
        self.phone = phone
        self.age = age
    
    def __repr__(self):
        return f"User username: {self.username}, name: {self.name}"
    
    def toJson(self):
        return {
            "username": self.username,
            "name": self.name,
            "phone": self.phone,
            "age": self.age
        }