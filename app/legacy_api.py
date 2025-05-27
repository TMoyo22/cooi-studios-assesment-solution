from flask import request, Response
from flask_restful import Resource

hvac_status = {"status": "inactive"}  # Example status


# Authentication
def check_auth(username, password):
    return username == "COOiLabs" and password == "123456"


def authenticate():
    return Response(
        "Could not verify your access level for that URL.\nInvalid credentials",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'},
    )


def requires_auth(f):
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    decorated.__name__ = f.__name__
    return decorated


# API Resources with authentication
class HVACStatus(Resource):
    @requires_auth  # API Resources with authentication
    def get(self):
        return hvac_status, 200


class HVACCommand(Resource):
    @requires_auth  # API Resources with authentication
    def post(self):
        data = request.get_json(force=True)
        command = data.get("command")

        if command == "activate":
            hvac_status["status"] = "active"
            return {"message": "HVAC activated"}, 200
        elif command == "deactivate":
            hvac_status["status"] = "inactive"
            return {"message": "HVAC deactivated"}, 200
        else:
            return {"error": "Invalid command"}, 400
