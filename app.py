#!/usr/bin/python

from datetime import timedelta
from flask_restful import Api
from flask import Flask, jsonify
from flask_jwt import JWT
from flask.ext.bcrypt import Bcrypt
from common.db import Storage
from resources.temperature import TemperatureController
from resources.user import UserController
from settings import debug_mode, db_uri, jwt_secret_key, jwt_expiration_delta_seconds
from errors import GenericException, InvalidUsage, UserAlreadyExists
from auth import Auth

def main():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = jwt_secret_key
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=jwt_expiration_delta_seconds)

    bcrypt = Bcrypt(app)
    storage = Storage(db_uri)
    auth = Auth(storage, bcrypt)
    jwt = JWT(app, auth.authenticate, auth.identity)

    api = Api(app)
    api.add_resource(TemperatureController, "/temp/",
        resource_class_kwargs={
            "storage": storage
    })
    api.add_resource(UserController, "/user/",
        resource_class_kwargs={
            "storage": storage,
            "bcrypt": bcrypt
    })

    @app.errorhandler(GenericException)
    @app.errorhandler(InvalidUsage)
    @app.errorhandler(UserAlreadyExists)
    def exception_handler(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    app.run(debug=debug_mode, host="0.0.0.0", port=4000)

if __name__ == "__main__":
    main()
