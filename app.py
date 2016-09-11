#!/usr/bin/python

from flask import Flask, jsonify
from flask_restful import Api
from resources.temperature import Temperature
from errors import InvalidUsage

app = Flask(__name__)
api = Api(app)
api.add_resource(Temperature, "/temp/")

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
