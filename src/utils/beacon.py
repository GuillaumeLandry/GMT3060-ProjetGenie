from datetime import datetime

class Beacon:
    def __init__(self, name, uid, description="Aucune"):
        self.name = name
        self.uid = uid
        self.description = description

        self.x = None
        self.y = None
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
        return (f'Nom de balise: {self.name}\n'
                f'UID: {self.uid}\n'
                f'Description: {self.description}\n'
                f'Distance: {self.distance} m\n')

