from flask import Flask, session, render_template

from auth import verify_token
from auth_blueprint import bp
from config import config
from database import db, UserDB
from exceptions import CustomException

app = Flask(__name__)

app.config["SECRET_KEY"] = config.secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = config.database_uri

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(bp, url_prefix="/auth")

@app.route("/")
def home():
    return "Public URL"

@app.route("/p1")
def private():
    try:
        user = verify_token()
        return f"Hi {user.username}, {user.name}"
    except CustomException as e:
        return e.response()
    except Exception as e:
        return {"message": "Exception "+str(e)}, 400


@app.route("/p2")
def private2():
    try:
        user = verify_token()
        return f"Hi {user.username}, {user.name}"
    except CustomException as e:
        return e.response()
    except Exception as e:
        return {"message": "Exception "+str(e)}, 400



