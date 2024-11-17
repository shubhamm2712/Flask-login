import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    secret_key = os.getenv("FLASK_SECRET_KEY")
    database_uri = os.getenv("DB_URI")

config = Config()