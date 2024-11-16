import os

from dotenv import load_dotenv
from flask import Flask, session, render_template

from auth_blueprint import bp
from database import db, UserDB

app = Flask(__name__)

load_dotenv()
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(bp, url_prefix="/auth")

@app.route("/")
def home():
    if "user" in session:
        return render_template("home.html", user = session["user"])
    return render_template("home.html")

