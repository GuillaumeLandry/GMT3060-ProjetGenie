from datetime import datetime

class Beacon:
    def __init__(self, name, mac):
        self.name = name
        self.mac = mac
        self.rssi = None
        self.rssi_kalman = None
        self.distance = None
        self.receiverDevice = None
        self.timestamp = datetime.min
        
    def set_beacon_on_location(self, location):
        self.x = location.x
        self.y = location.y

    def set_telemetry(self, timestamp, receiverDevice, rssi, rssi_kalman, distance):
        self.timestamp = datetime.fromtimestamp(int(timestamp)/1000.0)
        self.receiverDevice = receiverDevice
        self.rssi = rssi
        self.rssi_kalman = rssi_kalman
        self.distance = distance

    def reset(self):
        self.rssi = None
        self.rssi_kalman = None
        self.distance = None
        self.receiverDevice = None
        self.timestamp = datetime.min

    def __str__(self):
        return f'Beacon {self.name} : {self.distance} m'

