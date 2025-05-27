from flask import Flask
from flask_restful import Api
from app.legacy_api import HVACStatus, HVACCommand


def create_app():
    app = Flask(__name__)
    api = Api(app)

    # Legacy system endpoints
    api.add_resource(HVACStatus, "/api/hvac/status")
    api.add_resource(HVACCommand, "/api/hvac/command")

    return app
