from flask import request
from flask_restful import Resource

# Simulated HVAC system status (in-memory)
hvac_status = {"status": "inactive"}


class HVACStatus(Resource):
    def get(self):
        # Return current HVAC status
        return hvac_status, 200


class HVACCommand(Resource):
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
