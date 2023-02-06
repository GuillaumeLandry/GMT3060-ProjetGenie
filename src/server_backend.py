import json
from flask import jsonify

class Backend():
    def __init__(self):
        self.logging = False
        self.etude_name = "etude_1"
        self.data_ble = []
        self.timestamps = []
        self.graph_data = []

    def set_args(self, parser):
        self.logging = parser.parse_args().log


    def format_timestamp(self, timestamp):
        ts = timestamp.split(" ")
        ts = ts[-3].split(":")
        ts_float = float(ts[0]) + float(ts[1])/60 + float(ts[2])/3600

        return ts_float

    def process_data(self, request):
        timestamp = request.form["Timestamp"]
        receiverDevice = request.form["ReceiverDevice"]
        bleDevice = request.form["BLEDevice"]
        rssi = request.form["RSSI"]

        ts_float = self.format_timestamp(timestamp)

        self.data_ble.append({
            "Timestamp": float(ts_float),
            "ReceiverDevice": str(receiverDevice),
            "BLEDevice": str(bleDevice),
            "RSSI": float(rssi),
        })
        
        self.save_to_disk()
        
        return "received"

    def provide_data(self):
        data = []
        for elem in self.data_ble:
            if elem['BLEDevice'] == 'FC:CF:C5:18:B0:E8':
                if len(data) == 0 or elem['Timestamp'] > data[-1]['x']:
                    data.append({'x': elem["Timestamp"], 'y': elem["RSSI"]})

        return jsonify(data)

    def save_to_disk(self):
        if (self.logging == True):
            with open('./etudes/' + self.etude_name + '.txt', 'w') as fp:
                for packet in self.data_ble:
                    fp.write("%s\n" % packet)
            with open('./etudes/' + self.etude_name + '.json', 'w') as fp:
                json.dump(self.data_ble, fp, indent=4)