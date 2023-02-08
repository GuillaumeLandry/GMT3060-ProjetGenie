import argparse
import server_backend as server_backend
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)
backend = server_backend.Backend()

@app.route("/")
def render():
    return render_template('index.html', data_ble=2)

@app.route("/ble", methods=["POST"])
def process():
    return backend.process_data(request)

@app.route("/etude", methods=["POST"])
@cross_origin()
def update_params_etude():
    return backend.update_params_etude(request.json)

@app.route("/provide", methods=["GET"])
def provide():
    return backend.provide_data()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', action='store_true')
    backend.set_args(parser)

    app.run(host='0.0.0.0')