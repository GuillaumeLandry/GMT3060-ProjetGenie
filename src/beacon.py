from datetime import datetime
all_beacons = [
        {'name':1,
        'mac':'CA:F4:06:34:9C:31'},
        {'name':2,
        'mac':'D9:27:C2:C1:22:38'},
        {'name':3,
        'mac':'CC:B9:16:CD:6F:2F'},
        {'name':4,
        'mac':'FC:CF:C5:18:B0:E8'},

        {'name':5,
        'mac':'AJOUTER ICI MAC ADRESSE'},
        {'name':6,
        'mac':'AJOUTER ICI MAC ADRESSE2'},
    ]

def format_timestamp( timestamp):     
    dt = timestamp.split('EST ')
    datetime_str = dt[0] + dt[1]
    datetime_object = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y')
    return datetime_object

class Beacon:
    def __init__(self, name, mac):
        self.name = name
        self.mac = mac
        self.timestamp = datetime(year=2020, month=12, day=21, hour=12, minute=22, second=00)
        self.distance = 0
        
    def set_beacon_on_point(self, point):
        self.x = point.x
        self.y = point.y

    def myprint(self):
        return f"beacon {self.name}, {self.mac}_______________________{self.distance}"

    def set_telemetry(self, timestamp, receiverDevice, distance):
        self.timestamp = format_timestamp(timestamp)
        self.reciverDevice = receiverDevice
        self.distance = distance



