
from datetime import datetime
from beacon import Beacon, all_beacons
from points import get_used_points
from easy_trilateration.model import *  
from easy_trilateration.least_squares import easy_least_squares  
from easy_trilateration.graph import *  
import random

class Backend():
    def __init__(self):
        self.b1 = Beacon(all_beacons[0]['name'], all_beacons[0]['mac'])
        self.b2 = Beacon(all_beacons[1]['name'], all_beacons[1]['mac'])
        self.b3 = Beacon(all_beacons[2]['name'], all_beacons[2]['mac'])
        self.b4 = Beacon(all_beacons[3]['name'], all_beacons[3]['mac'])
        self.b5 = Beacon(all_beacons[4]['name'], all_beacons[4]['mac'])
        self.b6 = Beacon(all_beacons[5]['name'], all_beacons[5]['mac'])
        self.used_beacons = []
        self.received_beacons = []
        self.start_ = False
        self.params_setted = False

    def set_args(self, parser):
        self.logging = parser.parse_args().log

    def start_getting_data(self):
        if self.start_ == False and self.params_setted == True:
            self.start_ = True
            print('________________________START GETTING DATA_______________')

    def process_data(self, request):
        
        timestamp = request.form["Timestamp"]
        receiverDevice = request.form["ReceiverDevice"]
        bleDevice = request.form["BLEDevice"]
        rssi = request.form["RSSI"]
        
        # on peut creer une classe générale pour beacons et écrire ça dans une-deux lignes, au besoin
        if bleDevice == self.b1.mac:
            print("Received 1")
            self.b1.set_telemetry(timestamp, receiverDevice, self.calculate_distance_from_rssi(rssi))

        elif bleDevice == self.b2.mac:
            print("Received 2")
            self.b2.set_telemetry(timestamp, receiverDevice, self.calculate_distance_from_rssi(rssi))

        elif bleDevice == self.b3.mac:
            print("Received 3")
            self.b3.set_telemetry(timestamp, receiverDevice, self.calculate_distance_from_rssi(rssi))

        elif bleDevice == self.b4.mac:
            print("Received 4")
            self.b4.set_telemetry(timestamp, receiverDevice, self.calculate_distance_from_rssi(rssi))

        elif bleDevice == self.b5.mac:
            print("Received 5")
            self.b5.set_telemetry(timestamp, receiverDevice, self.calculate_distance_from_rssi(rssi))

        elif bleDevice == self.b6.mac:
            print("Received 6")
            self.b6.set_telemetry(timestamp, receiverDevice, self.calculate_distance_from_rssi(rssi))

        self.start_getting_data()
        return "received"

    def update_params_etude(self, request):

        new_params = request['params']

        if new_params["filename"] == "":
            print('________étude arrêtée________________')
            
            self.filename = new_params["filename"]
            self.params_setted = False
            
            return "ok"

        else:

            print('________params setted________________', new_params)
            points = get_used_points(new_params.values())
            
            for point in points:
                if new_params["B1"] == point.name:
                    self.b1.set_beacon_on_point(point)
                    self.used_beacons.append(self.b1)
                elif new_params["B2"] == point.name:
                    self.b2.set_beacon_on_point(point)
                    self.used_beacons.append(self.b2)
                elif new_params["B3"] == point.name:
                    self.b3.set_beacon_on_point(point)
                    self.used_beacons.append(self.b3)
                elif new_params["B4"] == point.name:
                    self.b4.set_beacon_on_point(point)
                    self.used_beacons.append(self.b4)
                elif new_params["B5"] == point.name:
                    self.b5.set_beacon_on_point(point)
                    self.used_beacons.append(self.b5)
                elif new_params["B6"] == point.name:
                    self.b6.set_beacon_on_point(point)
                    self.used_beacons.append(self.b6)
                else:
                    pass
                # throw error pas de pointe associée... qqch comme ça
            
            self.filename = new_params["filename"]
            self.params_setted = True

            return "ok"

    def calculate_distance_from_rssi(self, rssi):
        return float(10 **((-69 - int(rssi)) / 20))

    def essaye_calcul_position_parmi_les_listes_B1_B6(self):
        now = datetime.now()
        circles = []

        if len(self.used_beacons) >= 3: # minimum qu'on a besoin 
            for beacon in self.used_beacons:
                if beacon.mac == 'EB:76:88:9B:81:63':
                    print(beacon.timestamp)
                delta_seconds = abs((beacon.timestamp - now).total_seconds()  + 2.398774) # ce n'est pas bon
                if delta_seconds < 1:
                    circles.append(Circle(float(beacon.x), float(beacon.y), float(beacon.distance)))
            if len(circles) >= 3:
                position, _ = easy_least_squares(circles)      
                return position
            else: 
                return None 

    def provide_data(self):
        if self.params_setted and self.start_:
            data = [] # ici on peut faire self.data et accumuler la trajectoire
            position = self.essaye_calcul_position_parmi_les_listes_B1_B6()
            if position != None:
                data.append( {'x': position.center.x, 'y':position.center.y})
                with open('./etudes/' + self.filename + '.txt', 'a') as f:
                    f.write((f'x = {position.center.x}, y = {position.center.y},'
                             f'error = {position.radius}, time1 = {self.b1.timestamp},'
                             f'time2 = {self.b2.timestamp}, time3 = {self.b3.timestamp},'
                             f'time4 = {self.b4.timestamp}, time5 = {self.b5.timestamp},'
                             f'time6 = {self.b6.timestamp}\n'))
                return data
            else:
                print("No position")
                x= random.randint(200, 250)
                y= random.randint(200, 250)
                return [{'x':x, 'y':y}]
        elif self.params_setted:
            print("parametres sont settees, lance l'application")
            x= random.randint(10, 22)
            y= random.randint(10, 22)
            return [{'x':x, 'y':y}]
        else:
            print('not started yet')
            x= random.randint(50, 62)
            y= random.randint(50, 62)
            return [{'x':x, 'y':y}]

    def provide_map(self):
        data = [] # ici on peut faire self.data et accumuler la trajectoire

        with open("CARTO-LAB.txt", "r") as f:
            for num in f.readlines():
                num = num.split(",")
                x, y, z = [num[1], num[2], num[3]]
                data.append({'x': x, 'y':y})
        return data
