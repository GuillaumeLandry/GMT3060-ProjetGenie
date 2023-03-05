import logging
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin

from LocationServer import LocationServer

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)
backend = LocationServer()

@app.route("/")
def render():
    return render_template('index.html', data_ble=2)

@app.route("/ble", methods=["POST"])
def ble():
    return backend.process_incoming_data(request)

@app.route("/etude", methods=["POST"])
@cross_origin()
def etude():
    return backend.update_params_etude(request.json)

@app.route("/plot", methods=["POST"])
def plot():
    return backend.plot_study(request.json)

@app.route("/provide", methods=["GET"])
def provide():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    return backend.provide_data()

@app.route("/map-lab", methods=["GET"])
def map_lab():
    return backend.provide_map_lab()

@app.route("/map-danger", methods=["GET"])
def map_danger():
    return backend.provide_map_danger()

@app.route("/alert", methods=["GET"])
def alert():
    return backend.send_alert_flag()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
