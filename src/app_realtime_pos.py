import argparse

import dash
from dash.dependencies import Output, Input, State
from dash import html, dcc
from plotly.subplots import make_subplots

from flask import Flask, request
from flask_restful import Api
import plotly.express as px
import plotly

import json
import pandas as pd
from collections import deque
import plotly.graph_objs as go

# Variables globales
data_ble = []
X = deque(maxlen = 20)
X.append(1)
Y = deque(maxlen = 20)
Y.append(1)
devices = []
beacons = pd.read_csv("./beacons.txt", sep=" ", header=None)
points = pd.read_csv("./points.txt", sep=" ", header=None)
beacons_options = [{'label': beacons.at[i,0], 'value':beacons.at[i,0]} for i in range(len(beacons))]
points_options = [{'label': points.at[i,0], 'value':points.at[i,0]} for i in range(len(points))]
etude_en_cours = False
etude_name = "etude_1"

# Setup du serveur et de l'application 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = Flask('LocationServer')
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)
api = Api(server)

# Interface graphique de l'application
app.layout = html.Div([
    html.Div(id='placeholder1'),

    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
    ),
    html.H1('Tableau de bord'),
    html.P('Appareils connectés :'),
    html.Li(
        devices,
        value='Aucun appareil connecté',
        style={'margin': '1%'}
    ),
    html.Hr(),
    dcc.Checklist(
        options=beacons_options,
        style={'width': '10%', 'display': 'inline-block'}
    ),                
    dcc.Dropdown(
        options=points_options,
        id='crossfilter-xaxis-column',
        style={'width': '40%', 'display': 'inline-block'},
    ),
    dcc.Input(id="etude", type="text", placeholder="Nom de l'étude", style={'marginRight':'10px'}),
    html.Button(
        'Démarrer l\'étude',
        id="btn-start"
    ),
    html.Button(
        'Arrêter l\'étude',
        id="btn-stop"
    ),
    html.Hr(),
    html.Div([
        html.H4('Position de l\'utilisateur'),
        html.Div(id='live-indoor-text'),
        dcc.Graph(id='live-indoor-graph', animate=True),
    ]),
],style={'margin': '1%'})

@app.callback(
    Output('etude', 'value'),
    Input('btn-start', 'n_clicks'),
    State('etude', 'value')
)
def start_etude(n_clicks, value):
    global etude_en_cours
    etude_en_cours = True

    global etude_name
    etude_name = value

    return ""

@app.callback(
    Output('placeholder1', 'children'),
    Input('btn-stop', 'n_clicks'),
)
def stop_etude(n_clicks):
    global etude_en_cours
    etude_en_cours = False
    
    return ""

@app.callback(
    Output('live-indoor-text', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_indoor_text(n):
    style = {'padding': '5px', 'fontSize': '16px'}

    if (len(data_ble)) > 0:
        return [
            html.Span('Timestamp: {0}\n'.format((data_ble[-1]["Timestamp"])), style=style),
            html.Span('ReceiverDevice: {0}\n'.format((data_ble[-1]["ReceiverDevice"])), style=style),
            html.Span('BLEDevice: {0}\n'.format((data_ble[-1]["BLEDevice"])), style=style),
            html.Span('RSSI: {0:.2f}\n'.format((data_ble[-1]["RSSI"])), style=style),
        ]
    else :
        return html.Span('')

@app.callback(Output('live-indoor-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_indoor_graph(n):
    X=[]
    Y=[]

    data = plotly.graph_objs.Scatter(
        x=X,
        y=Y,
        name='Scatter',
        mode='lines+markers'
    )

    if (len(data_ble)>0):
        for elem in data_ble:
            if elem['BLEDevice'] == 'FC:CF:C5:18:B0:E8':
                X.append(elem['Timestamp'])
                Y.append(elem['RSSI'])


        data = plotly.graph_objs.Scatter(
            x=X,
            y=Y,
            name='Scatter',
            mode='lines+markers'
        )

        return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                    yaxis=dict(range=[min(Y), max(Y)]),
                                                    title='Flux RSSI de la balise ' + 'FC:CF:C5:18:B0:E8')}

    return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[0, 0]),
                                                    yaxis=dict(range=[0, 0]),
                                                    title='Flux RSSI de la balise ' + 'FC:CF:C5:18:B0:E8')}

@server.route("/ble", methods=["POST"])
def show_ble():
    timestamp = request.form["Timestamp"]
    receiverDevice = request.form["ReceiverDevice"]
    bleDevice = request.form["BLEDevice"]
    rssi = request.form["RSSI"]

    if (receiverDevice not in devices):
        devices.append(receiverDevice)

    ts = timestamp.split(" ")
    ts = ts[-3].split(":")
    ts_float = float(ts[0]) + float(ts[1])/60 + float(ts[2])/3600

    data_ble.append({
        "Timestamp": float(ts_float),
        "ReceiverDevice": str(receiverDevice),
        "BLEDevice": str(bleDevice),
        "RSSI": float(rssi),
    })
    
    if (parser.parse_args().log == True) :
        with open('./etudes/' + etude_name + '.txt', 'w') as fp:
            for packet in data_ble:
                fp.write("%s\n" % packet)
        with open('./etudes/' + etude_name + '.json', 'w') as fp:
            json.dump(data_ble, fp, indent=4)
    
    return "received"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', action='store_true')

    app.run_server(host='0.0.0.0', port=5000, debug=False)