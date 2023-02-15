import server_backend as server_backend
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import logging

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)
backend = server_backend.Backend()

@app.route("/")
def render():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
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
