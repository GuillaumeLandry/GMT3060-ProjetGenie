import argparse

import dash
from dash.dependencies import Output, Input
from dash import html, dcc

import plotly.express as px
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from flask import Flask, request
from flask_restful import Api

import datetime
import json
import random
import pandas as pd
from collections import deque
from pyorbital.orbital import Orbital

import asyncio
from bleak import BleakScanner


# Variables globales
#satellite = Orbital('TERRA')
data_packets = [{"X": 0, "Y": 0, "msg": "Init"}]
data_ble = [{"ID": 0, "RSSI": 0}]
X = deque(maxlen = 20)
X.append(1)
Y = deque(maxlen = 20)
Y.append(1)
df = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

# Setup du serveur et de l'application 
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
server = Flask('LocationServer')
app = dash.Dash(__name__, server=server, external_stylesheets=external_stylesheets)
api = Api(server)

# Interface graphique de l'application
app.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
    ),
    #html.Div([
    #    html.H4('TERRA Satellite Live Feed'),
    #    html.Div(id='live-update-text'),
    #    dcc.Graph(id='live-update-graph'),
    #]),
    dcc.RadioItems(
        ['Linear', 'Log'],
        'Linear',
        id='crossfilter-xaxis-type',
        labelStyle={'display': 'inline-block', 'marginTop': '5px'}
    ),
    dcc.ConfirmDialogProvider(
        children=html.Button(
            'Click Me',
        ),
        id='danger-danger',
        message='Danger danger! Are you sure you want to continue?'
    ),
    dcc.Dropdown(
        df['Indicator Name'].unique(),
        'Fertility rate, total (births per woman)',
        id='crossfilter-xaxis-column',
    ),
    html.Div(
        className="trend",
        children=[
            html.Ul(id='my-list', children=[html.Li(i) for i in data_packets])
        ],
    ),
    html.Div([
        html.H4('Live Feed Indoor Location Feed'),
        html.Div(id='live-indoor-text'),
        dcc.Graph(id='live-indoor-graph'),
    ]),
])

#async def run_ble_scan():
#    devices = await BleakScanner.discover()
#    for d in devices:
#        print(d, d.name, d.rssi)
#
#    data_rssi.append(devices[0].rssi)
#
#    loop = asyncio.get_event_loop()
#    loop.run_until_complete(run_ble_scan())
#
#    data_rssi.append(devices[0].rssi)

# Série de callbacks utilisés
@app.callback(
    Output('live-indoor-text', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_indoor_text(n):
    style = {'padding': '5px', 'fontSize': '16px'}

    return [
        html.Span('Dernier X: {0:.2f}'.format(data_packets[-1]["X"]), style=style),
        html.Span('Dernier Y: {0:.2f}'.format(data_packets[-1]["Y"]), style=style),
        html.Span('Message: {0}'.format(data_packets[-1]["msg"]), style=style),
        html.Span('ID dernier BLE: {0}'.format((data_ble[-1]["ID"])), style=style),
        html.Span('RSSI dernier BLE: {0:.2f}'.format((data_ble[-1]["RSSI"])), style=style),
    ]
@app.callback(Output('live-indoor-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_indoor_graph(n):
    data = {
        'time': [],
        'X': [],
        'Y': [],
    }

    data['X'].append(data_packets[-1]["X"])
    data['Y'].append(data_packets[-1]["Y"])

    fig = make_subplots(rows=1, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': data["X"],
        'y': data["Y"],
        'name': 'Altitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)

    return fig

#@app.callback(Output('live-update-text', 'children'),
#              Input('interval-component', 'n_intervals'))
#def update_metrics(n):
#    lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
#    style = {'padding': '5px', 'fontSize': '16px'}
#    return [
#        html.Span('Longitude: {0:.2f}'.format(lon), style=style),
#        html.Span('Latitude: {0:.2f}'.format(lat), style=style),
#        html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
#    ]


# Multiple components can update everytime interval gets fired.
#@app.callback(Output('live-update-graph', 'figure'),
#              Input('interval-component', 'n_intervals'))
#def update_graph_live(n):
#    satellite = Orbital('TERRA')
#    data = {
#        'time': [],
#        'Latitude': [],
#        'Longitude': [],
#        'Altitude': []
#    }
#
#    # Collect some data
#    for i in range(180):
#        time = datetime.datetime.now() - datetime.timedelta(seconds=i*20)
#        lon, lat, alt = satellite.get_lonlatalt(
#            time
#        )
#        data['Longitude'].append(lon)
#        data['Latitude'].append(lat)
#        data['Altitude'].append(alt)
#        data['time'].append(time)
#
#    # Create the graph with subplots
#    fig = plotly.subplots.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
#    fig['layout']['margin'] = {
#        'l': 30, 'r': 10, 'b': 30, 't': 10
#    }
#    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
#
#    fig.append_trace({
#        'x': data['time'],
#        'y': data['Altitude'],
#        'name': 'Altitude',
#        'mode': 'lines+markers',
#        'type': 'scatter'
#    }, 1, 1)
#    fig.append_trace({
#        'x': data['Longitude'],
#        'y': data['Latitude'],
#        'text': data['time'],
#        'name': 'Longitude vs Latitude',
#        'mode': 'lines+markers',
#        'type': 'scatter'
#    }, 2, 1)
#
#    return fig

# Endpoint qui gère les données provenant de l'application Android
@server.route("/debug", methods=["POST"])
def show_debug():
    coordX = request.form["coordX"]
    coordY = request.form["coordY"]
    msg = request.form["msg"]
    print("Received (" + coordX + ", " + coordY + ")" + " with the following message : " + msg)

    data_packets.append({
        "X": float(coordX),
        "Y": float(coordY),
        "msg": str(msg)
    })
    
    #with open('./received_data/data_packets.txt', 'w') as fp:
    #    for packet in data_packets:
    #        # write each item on a new line
    #        fp.write("%s\n" % packet)
    if (parser.parse_args().log == True) :
        with open('./received_data/data_packets.json', 'w') as fp:
            json.dump(data_packets, fp, indent=4)
    
    return "received"

@server.route("/ble", methods=["POST"])
def show_ble():
    id = request.form["ID"]
    rssi = request.form["RSSI"]

    data_ble.append({
        "ID": str(id),
        "RSSI": float(rssi),
    })
    
    #with open('./received_data/data_ble.txt', 'w') as fp:
    #    for packet in data_ble:
    #        # write each item on a new line
    #        fp.write("%s\n" % packet)
    if (parser.parse_args().log == True) :
        with open('./received_data/data_ble.json', 'w') as fp:
            json.dump(data_ble, fp, indent=4)
    
    return "received"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', action='store_true')

    app.run_server(host='0.0.0.0', port=5000, debug=False)