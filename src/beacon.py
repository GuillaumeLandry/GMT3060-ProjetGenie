from datetime import datetime
all_beacons = [
        {'name':1,
        'mac':'CA:F4:06:34:9C:31'}, # Alexandre - 
        {'name':2,
        'mac':'D9:27:C2:C1:22:38'}, # Alexandre - 
        {'name':3,
        'mac':'CC:B9:16:CD:6F:2F'}, # Alexandre - 
        {'name':4,
        'mac':'F6:C1:78:1C:4F:2D'}, # Guillaume - Jaune (F3:BE:75:19:47:2A)
        {'name':5, 
        'mac':'EB:76:88:9B:81:63'}, # Guillaume - Rose (27:EA:9B:C3:34:B0)
        {'name':6,
        'mac':'FD:D0:C6:19:B1:E9'}, # Guillaume - Mauve (FA:CD:C3:16:AE:E6) (3C:C8:89:AB:A2:38)
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
        self.timestamp = 0
        self.distance = 0
        
    def set_beacon_on_point(self, point):
        self.x = point.x
        self.y = point.y

    def myprint(self):
        return f"beacon {self.name}, {self.mac}_______________________{self.distance}"

    def set_telemetry(self, timestamp, receiverDevice, distance):
        self.timestamp = format_timestamp(timestamp)
        self.receiverDevice = receiverDevice
        self.distance = distance



