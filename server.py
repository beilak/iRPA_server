from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

''' Load all files'''
import importlib

importlib.import_module("services")
from services import *

''' Server setings '''
app = Flask(__name__)
# CORS(app, support_credentials=True)

@app.route('/api/<service>', methods=['POST', 'GET', 'OPTIONS'])
def add_message(service):
    result = call_service(service, request)
    return result


if __name__ == "__main__":
    app.run()
