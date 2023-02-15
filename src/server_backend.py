
from datetime import datetime
from beacon import Beacon, all_beacons
from points import get_used_points
from easy_trilateration.model import *  
from easy_trilateration.least_squares import easy_least_squares  
from easy_trilateration.graph import *  
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

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
        self.used_for_calculation_beacons = []
        self.start_ = False
        self.params_setted = False
        self.position_data = []
        self.danger_zone = Polygon()
        self.POSITION_HISTORY_SIZE = 20
        self.alert_flag = False
    
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
            print("Received 1 :", rssi) # Distance 3.70m
            with open('./etudes/RSSI_values/' + 'b1' + '.txt', 'a') as f:
                f.write(f'{rssi}\n')
            self.b1.set_telemetry(timestamp, receiverDevice, self.calculate_distance_from_rssi(rssi))
        elif bleDevice == self.b2.mac:
            print("Received 2 :", rssi) # Distance 6.10m
            with open('./etudes/RSSI_values/' + 'b2' + '.txt', 'a') as f:
                f.write(f'{rssi}\n')
            self.b2.set_telemetry(timestamp, receiverDevice, self.calculate_distance_from_rssi(rssi))
        elif bleDevice == self.b3.mac:
            print("Received 3 :", rssi) # Distance 5.00m
            with open('./etudes/RSSI_values/' + 'b3' + '.txt', 'a') as f:
                f.write(f'{rssi}\n')
            self.b3.set_telemetry(timestamp, receiverDevice, self.calculate_distance_from_rssi(rssi))
        elif bleDevice == self.b4.mac:
            print("Received 4 :", rssi) # Distance 4.50m
            with open('./etudes/RSSI_values/' + 'b4' + '.txt', 'a') as f:
                f.write(f'{rssi}\n')
            self.b4.set_telemetry(timestamp, receiverDevice, self.calculate_distance_from_rssi(rssi))
        elif bleDevice == self.b5.mac:
            print("Received 5 :", rssi) # Distance 6.40m
            with open('./etudes/RSSI_values/' + 'b5' + '.txt', 'a') as f:
                f.write(f'{rssi}\n')
            self.b5.set_telemetry(timestamp, receiverDevice, self.calculate_distance_from_rssi(rssi))
        elif bleDevice == self.b6.mac:
            print("Received 6 :", rssi) # Distance 3.50m
            with open('./etudes/RSSI_values/' + 'b6' + '.txt', 'a') as f:
                f.write(f'{rssi}\n')
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
        # Version 2
        # friis_transmission_constant = 41.2
        # tx_power = 10
        # path_loss_exponent = 2 # =2 dans un environnement libre. Probablement plus haut en intérieur
        # return 10**((tx_power - int(rssi) - friis_transmission_constant) / (10 * path_loss_exponent))
        
        # Version 3
        # tx_power = 10
        # return float(10**((tx_power-int(rssi))/40))

        # Version 1 (https://iotandelectronics.wordpress.com/2016/10/07/how-to-calculate-distance-from-the-rssi-value-of-the-ble-beacon/)
        # https://community.estimote.com/hc/en-us/articles/201636913-What-are-Broadcasting-Power-RSSI-and-other-characteristics-of-a-beacon-s-signal-        
        measured_power = -37 # Default -69 | (Voir fichier Excel pour explication de cette valeur)
        path_loss_exponent = 4 # =2 dans un environnement libre. Probablement plus haut en intérieur entre [2,4]
        return float(10**((measured_power - int(rssi)) / (10 * path_loss_exponent)))

    def essaye_calcul_position_parmi_les_listes_B1_B6(self):
        now = datetime.now()
        circles = []
        self.used_for_calculation_beacons = []

        if len(self.used_beacons) >= 3: # minimum qu'on a besoin 
            for beacon in self.used_beacons:
                if beacon.timestamp != None:
                    delta_seconds = abs((beacon.timestamp - now).total_seconds() + 2.398774) # ce n'est pas bon
                    if delta_seconds < 1:
                        circles.append(Circle(float(beacon.x), float(beacon.y), float(beacon.distance)))
                        self.used_for_calculation_beacons.append(beacon)
                    else:
                        beacon.reset()

            if len(circles) >= 3:
                position, _ = easy_least_squares(circles)
                return position
            else: 
                return None

    def provide_data(self):
        if self.params_setted and self.start_:
            position = self.essaye_calcul_position_parmi_les_listes_B1_B6()
            now = datetime.now()
            if position != None:

                ## Process danger zone alert
                if self.danger_zone.contains(Point(position.center.x,position.center.y)):
                    self.alert_flag = True
                
                self.position_data.append({'x':position.center.x, 'y':position.center.y})
                with open('./etudes/' + self.filename + '.txt', 'a') as f:
                    f.write(f'timestamp={now},x={position.center.x},y={position.center.y},error={position.radius},')
                    for beacon in self.used_for_calculation_beacons:
                        f.write(f'dist{beacon.name}={beacon.distance},time{beacon.name}={beacon.timestamp},')
                    f.write('\n')

        while len(self.position_data) > self.POSITION_HISTORY_SIZE:
            self.position_data.pop(0)

        return self.position_data

    def provide_map_lab(self):
        data = []
        with open("carte_lab.txt", "r") as f:
            for num in f.readlines():
                num = num.split(",")
                x, y, z = [num[1], num[2], num[3]]
                data.append({'x': x, 'y':y})
        return data

    def provide_map_danger(self):
        data = []
        xy_list = []
        with open("carte_danger.txt", "r") as f:
            for num in f.readlines():
                num = num.split(",")
                x, y, z = [num[1], num[2], num[3]]

                xy_list.append(Point(x,y))
                data.append({'x':num[1],'y':num[2]})

        # xy_list.append(Point(98,91))
        # xy_list.append(Point(98,99))
        # xy_list.append(Point(103,99))
        # xy_list.append(Point(103,91))
        # xy_list.append(Point(98,91))
        # data.append({'x':98,'y':91})
        # data.append({'x':98,'y':99})
        # data.append({'x':103,'y':99})
        # data.append({'x':103,'y':91})
        # data.append({'x':98,'y':91})
        # self.danger_zone = Polygon(xy_list)

        return data
    
    def send_alert_flag(self):
        if self.alert_flag == True:
            self.alert_flag = False
            return {'alert': 'alert'}
        else:
            return {'alert': ''}
