from flask import make_response

class CustomException(Exception):
    def __init__(self, msg, status_code = 400):
        self.message = msg
        self.statusCode = status_code

    def response(self):
        return make_response({"message": self.message}, self.statusCode)