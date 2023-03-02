
import os
import json
import numpy as np
from datetime import datetime

from easy_trilateration.model import *  
from easy_trilateration.least_squares import easy_least_squares  
from easy_trilateration.graph import *  
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from plot_study import DataPlotter

from utils.beacon import Beacon, all_beacons
from utils.points import get_used_points
from utils.particle_filter import particle_filter
from utils.kalman_filter import KalmanFilter

class Backend():
    def __init__(self):
        # Beacons disponibles
        self.b1 = Beacon(all_beacons[0]['name'], all_beacons[0]['mac'])
        self.b2 = Beacon(all_beacons[1]['name'], all_beacons[1]['mac'])
        self.b3 = Beacon(all_beacons[2]['name'], all_beacons[2]['mac'])
        self.b4 = Beacon(all_beacons[3]['name'], all_beacons[3]['mac'])
        self.b5 = Beacon(all_beacons[4]['name'], all_beacons[4]['mac'])
        self.b6 = Beacon(all_beacons[5]['name'], all_beacons[5]['mac'])
        
        # Listes et autres structures
        self.used_beacons = []
        self.data_positions = []
        self.danger_zone = Polygon()

        # Flags
        self.etude_running = False
        self.alert_flag = False

        # Constantes globales
        self.POSITION_HISTORY_SIZE = 6

        # Filtres
        
        process_noise = 0.008 # Kalman -> Default : 0.008
        measurement_noise = 0.1 # Kalman -> Default : 0.1
        self.path_loss_exponent = 1.75 # RSSI_Dist -> =2 dans un environnement libre. Probablement plus haut en intérieur entre [2,4]
        self.minimum_accepted_rssi = -64.0 # -64.0 est environ 7m, au-dessous les données ne font plus de sens

        self.kalman1 = KalmanFilter(process_noise, measurement_noise)
        self.kalman2 = KalmanFilter(process_noise, measurement_noise)
        self.kalman3 = KalmanFilter(process_noise, measurement_noise)
        self.kalman4 = KalmanFilter(process_noise, measurement_noise)
        self.kalman5 = KalmanFilter(process_noise, measurement_noise)
        self.kalman6 = KalmanFilter(process_noise, measurement_noise)
        self.kalman_dist = KalmanFilter(process_noise, measurement_noise)

    def process_data(self, request):
        
        timestamp = request.form["Timestamp"]
        receiverDevice = request.form["ReceiverDevice"]
        bleDevice = request.form["BLEDevice"]
        rssi = request.form["RSSI"]

        # on peut creer une classe générale pour beacons et écrire ça dans une-deux lignes, au besoin
        if bleDevice == self.b1.mac:
            print("Received 1 :", rssi) # Distance 3.70m
            rssi_kalman = str(self.kalman1.kalman_filter(float(rssi)))
            self.b1.set_telemetry(timestamp, receiverDevice, rssi, rssi_kalman, self.calculate_distance_from_rssi(rssi_kalman))
        elif bleDevice == self.b2.mac:
            print("Received 2 :", rssi) # Distance 6.10m
            rssi_kalman = str(self.kalman2.kalman_filter(float(rssi)))
            self.b2.set_telemetry(timestamp, receiverDevice, rssi, rssi_kalman, self.calculate_distance_from_rssi(rssi_kalman))
        elif bleDevice == self.b3.mac:
            print("Received 3 :", rssi) # Distance 5.00m
            rssi_kalman = str(self.kalman3.kalman_filter(float(rssi)))
            self.b3.set_telemetry(timestamp, receiverDevice, rssi, rssi_kalman, self.calculate_distance_from_rssi(rssi_kalman))
        elif bleDevice == self.b4.mac:
            print("Received 4 :", rssi) # Distance 4.50m
            rssi_kalman = str(self.kalman4.kalman_filter(float(rssi)))
            self.b4.set_telemetry(timestamp, receiverDevice, rssi, rssi_kalman, self.calculate_distance_from_rssi(rssi_kalman))
        elif bleDevice == self.b5.mac:
            print("Received 5 :", rssi) # Distance 6.40m
            rssi_kalman = str(self.kalman5.kalman_filter(float(rssi)))
            self.b5.set_telemetry(timestamp, receiverDevice, rssi, rssi_kalman, self.calculate_distance_from_rssi(rssi_kalman))
        elif bleDevice == self.b6.mac:
            print("Received 6 :", rssi) # Distance 3.50m
            rssi_kalman = str(self.kalman6.kalman_filter(float(rssi)))
            self.b6.set_telemetry(timestamp, receiverDevice, rssi, rssi_kalman, self.calculate_distance_from_rssi(rssi_kalman))
        
        return "received"

    def update_params_etude(self, request):

        new_params = request['params']

        if new_params["filename"] == "":
            print('\nÉtude arrêtée.\n')
            self.etude_name = new_params["filename"]
            self.etude_running = False
            return "ok"

        else:
            print(f'\nParamètres mis à jour : {new_params}\nEnregistrement de l\'étude en cours ...\n')
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
            
            self.etude_name = new_params["filename"]
            self.etude_running = True

            return "ok"

    def calculate_distance_from_rssi(self, rssi):
        # (https://iotandelectronics.wordpress.com/2016/10/07/how-to-calculate-distance-from-the-rssi-value-of-the-ble-beacon/)
        # https://community.estimote.com/hc/en-us/articles/201636913-What-are-Broadcasting-Power-RSSI-and-other-characteristics-of-a-beacon-s-signal-        
        measured_power = -48 # Default -69 | (Voir fichier Excel pour explication de cette valeur)

        if float(rssi) < self.minimum_accepted_rssi:
            return None

        return float(10**((measured_power - float(rssi)) / (10 * self.path_loss_exponent)))
    
    def calcule_position(self, kalman_filtering=False):
        if len(self.used_beacons) >= 3: # minimum qu'on a besoin 
            now = datetime.now()
            circles = []

            for beacon in self.used_beacons:
                if beacon.distance != None:
                    delta_seconds = abs((beacon.timestamp - now).total_seconds() + 2.398774) # ce n'est pas bon
                    #if delta_seconds < 1:
                    #if kalman_filtering:
                    #    beacon.rssi_kalman = str(self.kalman.kalman_filter(float(beacon.rssi)))

                    circles.append(Circle(float(beacon.x), float(beacon.y), float(beacon.distance)))
                    #else:
                    #    beacon.reset()

            if len(circles) >= 3:
                position, _ = easy_least_squares(circles)
                return [position.center.x, position.center.y, position.radius]
            else: 
                return None

    def calcule_position_avec_filtrage(self, kalman_filtering=False):
        if len(self.used_beacons) >= 3:
            now = datetime.now()

            rssi_values = []
            beacons = []
            for beacon in self.used_beacons:
                if beacon.distance != None:
                    delta_seconds = abs((beacon.timestamp - now).total_seconds() + 2.398774)
                    if delta_seconds < 1:
                        # Change les valeurs de RSSI avec les résultats du filtre de kalman (sera ainsi modifié dans les logs)
                        if kalman_filtering == True:
                            beacon.rssi_kalman = str(self.kalman.kalman_filter(float(beacon.rssi)))
                            rssi_values.append(float(beacon.rssi_kalman))
                        else:
                            rssi_values.append(float(beacon.rssi))
                        
                        beacons.append((float(beacon.x), float(beacon.y)))
                    else:
                        beacon.reset()
            
            if len(rssi_values) > 0 and len(beacons) > 0:
                print(rssi_values)
                print(beacons)
                position = particle_filter(measurements=rssi_values, beacons=beacons)
                return [position[0], position[1], 0] # [x, y, erreur] (0=inconnu)
            else:
                return None

    def provide_data(self):
        if self.etude_running:
            position = self.calcule_position(kalman_filtering=True)
            # position = self.calcule_position_avec_filtrage(kalman_filtering=True)            
            
            if position is not None:
                ## Process danger zone alert
                if self.danger_zone.contains(Point(position[0],position[1])):
                    self.alert_flag = True
                
                # Append data and save to disk
                self.data_positions.append({'x':position[0], 'y':position[1]})
                self.log_to_disk(position)

        while len(self.data_positions) > self.POSITION_HISTORY_SIZE:
            self.data_positions.pop(0)

        return self.data_positions

    def provide_map_lab(self):
        data = []
        with open("./cartographies/carte_lab.txt", "r") as f:
            for num in f.readlines():
                num = num.split(",")
                x, y, z = [num[1], num[2], num[3]]
                data.append({'x': x, 'y':y})
        return data

    def provide_map_danger(self):
        data = []
        xy_list = []
        with open("./cartographies/carte_danger.txt", "r") as f:
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
        self.danger_zone = Polygon(xy_list)

        return data
    
    def send_alert_flag(self):
        if self.alert_flag == True:
            self.alert_flag = False
            return {'alert': 'alert'}
        else:
            return {'alert': ''}

    def log_to_disk(self, position):
        data = [{
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            'position': {
                'x': position[0],
                'y': position[1],
                'error': position[2]
            },
            'beacons': {
                self.b1.name: {
                    'rssi':self.b1.rssi,
                    'rssi_kalman':self.b1.rssi_kalman,
                    'dist':self.b1.distance,
                    'timestamp':self.b1.timestamp.strftime('%H:%M:%S.%f')[:-3]
                },
                self.b2.name: {
                    'rssi':self.b2.rssi,
                    'rssi_kalman':self.b2.rssi_kalman,
                    'dist':self.b2.distance,
                    'timestamp':self.b2.timestamp.strftime('%H:%M:%S.%f')[:-3]
                },
                self.b3.name: {
                    'rssi':self.b3.rssi,
                    'rssi_kalman':self.b3.rssi_kalman,
                    'dist':self.b3.distance,
                    'timestamp':self.b3.timestamp.strftime('%H:%M:%S.%f')[:-3]
                },
                self.b4.name: {
                    'rssi':self.b4.rssi,
                    'rssi_kalman':self.b4.rssi_kalman,
                    'dist':self.b4.distance,
                    'timestamp':self.b4.timestamp.strftime('%H:%M:%S.%f')[:-3]
                },
                self.b5.name: {
                    'rssi':self.b5.rssi,
                    'rssi_kalman':self.b5.rssi_kalman,
                    'dist':self.b5.distance,
                    'timestamp':self.b5.timestamp.strftime('%H:%M:%S.%f')[:-3]
                },
                self.b6.name: {
                    'rssi':self.b6.rssi,
                    'rssi_kalman':self.b6.rssi_kalman,
                    'dist':self.b6.distance,
                    'timestamp':self.b6.timestamp.strftime('%H:%M:%S.%f')[:-3]
                }
            }
        }]

        output_dir = f'./etudes/{self.etude_name}'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(f'{output_dir}/{self.etude_name}.json', 'a') as f:
            json.dump(data, f)
            f.write('\n')

    def plot_study(self, request):
        try:
            plotter = DataPlotter(request['params']['filename'])
            plotter.create_and_export_stats()
            return "exporté"
        except:
            return "erreur"