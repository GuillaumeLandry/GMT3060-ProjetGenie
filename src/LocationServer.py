
import os
import json
import csv
from datetime import datetime

from easy_trilateration.model import *  
from easy_trilateration.least_squares import easy_least_squares  
from easy_trilateration.graph import *  
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

from utils.Beacon import Beacon
from utils.MapLocation import MapLocation
from utils.ParticleFilter import ParticleFilter
from utils.KalmanFilter import KalmanFilter
from utils.StudyPlotter import StudyPlotter

class LocationServer():
    def __init__(self):
        # Constantes globales
        self.POSITION_HISTORY_SIZE = 6      # Affichage -> Affiche les X dernières positions calculées sur la carte
        self.MIN_REQUIRED_TRILATERATION = 3 # Trilatération -> Besoin de X distances ou plus pour calculer une position

        self.PROCESS_NOISE = 0.008          # Kalman -> Default : 0.008
        self.MEASUREMENT_NOISE = 0.1        # Kalman -> Default : 0.1
        
        self.MEASURED_POWER = -48           # RSSI Dist -> Default -69 | (Voir fichier Excel pour explication de cette valeur)
        self.PATH_LOSS_EXPONENT = 1.75      # RSSI_Dist -> =2 dans un environnement libre. Probablement plus haut en intérieur entre [2,4]
        self.MIN_ACCEPTED_RSSI = -64.0      # RSSI_Dist -> -64.0 est environ 7m, au-dessous les données ne font plus de sens

        # Variables globales
        self.available_beacons = self.load_beacons()
        self.map_locations = self.load_map_locations()
        self.etude_name = ""
        self.data_positions = []
        self.danger_zone = Polygon()

        # Flags
        self.ETUDE_RUNNING = False
        self.ALERT_FLAG = False

    def load_map_locations(self):
        locations = []
        with open('./cartographies/carte_original.txt', 'r') as file:
            for line in file:
                name, x, y, z = line.strip().split(',')
                locations.append(MapLocation(name, x, y, z))
        return locations

    def load_beacons(self):
        with open('./available_beacons.txt', 'r') as file:
            reader = csv.reader(file)
            next(reader) # Passe la première ligne, qui est l'entête du fichier
            beacons = {}
            for row in reader:
                name = row[0]
                uid = row[1]
                description = row[2]
                beacons[uid] = (Beacon(name, uid, description), KalmanFilter(self.PROCESS_NOISE, self.MEASUREMENT_NOISE))
        return beacons

    def provide_map_lab(self):
        data = []
        with open("./cartographies/carte_lab.txt", "r") as f:
            for line in f.readlines():
                x, y, z = line.strip().split(",")[1:4]
                data.append({'x': x, 'y':y})
        return data

    def provide_map_danger(self):
        data = []
        xy_list = []
        with open("./cartographies/carte_danger.txt", "r") as f:
            for line in f.readlines():
                x, y, z = line.strip().split(",")[1:4]
                xy_list.append(Point(x,y))
                data.append({'x':x,'y':y})

        self.danger_zone = Polygon(xy_list)
        return data

    def process_incoming_data(self, request):
        timestamp = request.form["Timestamp"]
        receiverDevice = request.form["ReceiverDevice"]
        bleDevice = request.form["BLEDevice"]
        rssi = request.form["RSSI"]

        if bleDevice in self.available_beacons:
            beacon, kalman_filter = self.available_beacons[bleDevice]
            rssi_kalman = str(kalman_filter.filter(float(rssi)))
            beacon.set_telemetry(timestamp, receiverDevice, rssi, rssi_kalman, self.calculate_distance_from_rssi(rssi_kalman))
        
        return "received"

    def calculate_distance_from_rssi(self, rssi):
        if float(rssi) < self.MIN_ACCEPTED_RSSI:
            return None

        return float(10**((self.MEASURED_POWER - float(rssi)) / (10 * self.PATH_LOSS_EXPONENT)))

    def update_params_etude(self, request):
        params_etude = request['params']

        if params_etude["filename"] == "":
            self.etude_name = params_etude["filename"]
            self.ETUDE_RUNNING = False
            print('\nÉtude arrêtée.\n')
            return "ok"

        else:            
            for _, (beacon, _) in self.available_beacons.items():
                map_location = next((location for location in self.map_locations if params_etude[f"B{beacon.name}"] == location.name), None)
                if map_location is not None:
                    beacon.set_beacon_on_location(map_location)
                else:
                    beacon.reset()

            self.etude_name = params_etude["filename"]
            self.data_logger = DataLogger(self.etude_name, self.available_beacons)
            self.ETUDE_RUNNING = True
            print(f'\nParamètres mis à jour : {params_etude}\nEnregistrement de l\'étude en cours ...\n')
            return "ok"
    
    def calculate_position_trilateration(self):
        circles = []
        for _, (beacon, _) in self.available_beacons.items():
            if beacon.distance is not None:
                circles.append(Circle(beacon.x, beacon.y, beacon.distance))

        if len(circles) >= self.MIN_REQUIRED_CIRCLES_TRILATERATION:
            position, _ = easy_least_squares(circles)
            return [position.center.x, position.center.y, position.radius]
        else: 
            return None

    def provide_data(self):
        if self.ETUDE_RUNNING:
            position = self.calculate_position_trilateration()
            
            if position is not None:
                ## Process danger zone alert
                if self.danger_zone.contains(Point(position[0],position[1])):
                    self.ALERT_FLAG = True
                
                # Append data and save to disk
                self.data_positions.append({'x':position[0], 'y':position[1]})
                self.data_logger.save_to_disk(position)

        if len(self.data_positions) > self.POSITION_HISTORY_SIZE:
            self.data_positions.pop(0)

        return self.data_positions
    
    def send_alert_flag(self):
        if self.ALERT_FLAG == True:
            self.ALERT_FLAG = False
            return {'alert': 'alert'}
        else:
            return {'alert': ''}

    def plot_study(self, request):
        try:
            plotter = StudyPlotter(request['params']['filename'])
            plotter.process_plots()
            return "exporté"
        except:
            return "erreur"