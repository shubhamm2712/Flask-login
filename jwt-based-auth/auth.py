from datetime import datetime, timedelta
from flask import request
import jwt

from config import config
from exceptions import CustomException
from database import UserDB

def generate_token(user):
    exp = datetime.now() + timedelta(minutes=3)
    payload = {
        "user":user.toJson(),
        "exp": exp.timestamp()
    }
    token = jwt.encode(payload,config.secret_key,algorithm="HS256")
    return token

def verify_token():
    if "Authorization" not in request.headers:
        print("herere")
        raise CustomException("Authentication required", 401)
    auth = request.headers["Authorization"]
    if " " not in auth:
        raise CustomException("Invalid authentication", 401)
    bearer,token = auth.split(" ")
    token = token.strip()
    if bearer != "Bearer":
        raise CustomException("Bearer token required", 401)
    if token is None:
        raise CustomException("Token is missing", 401)
    try:
        payload = jwt.decode(token,config.secret_key,algorithms=["HS256"])
        userJson = payload["user"]
        try:
            user = UserDB(**userJson)
            return user
        except e:
            raise CustomException("Invalid Payload "+str(e), 401)
    except jwt.ExpiredSignatureError as e:
        raise CustomException("Access token is expired", 401)
    except KeyError as e:
        raise CustomException("Invalid payload to token", 401)
    except Exception as e:
        raise CustomException("Invalid Token "+str(e), 401)
    

