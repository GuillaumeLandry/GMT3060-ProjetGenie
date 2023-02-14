import argparse
import server_backend as server_backend
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import logging

app = Flask(__name__, template_folder='templates', static_folder='static')
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
CORS(app)
backend = server_backend.Backend()

@app.route("/")
def render():
    return render_template('index.html', data_ble=2)

@app.route("/ble", methods=["POST"])
def ble():
    return backend.process_data(request)

@app.route("/etude", methods=["POST"])
@cross_origin()
def etude():
    return backend.update_params_etude(request.json)

@app.route("/provide", methods=["GET"])
def provide():
    return backend.provide_data()

@app.route("/map", methods=["GET"])
def map():
    return backend.provide_map()

if __name__ == "__main__":
    app.run(host='0.0.0.0')