import os
import json
from datetime import datetime

class DataLogger:
    def __init__(self, etude_name, available_beacons, output_dir, description=""):
        self.etude_name = etude_name
        self.available_beacons = available_beacons
        self.output_dir = output_dir
        self.description = description

    def save_to_disk(self, position, measured_power, path_loss_exponent):
        data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            'etude_name': self.etude_name,
            'description': self.description,
            'cst_measured_power': measured_power,
            'cst_path_loss_exponent': path_loss_exponent,
            'position': {
                'x': position[0],
                'y': position[1],
                'error': position[2]
            },
            'beacons': {}
        }

        for _, (beacon, kalman) in self.available_beacons.items():
            data['beacons'][beacon.name] = {
                'rssi': beacon.rssi,
                'rssi_kalman': beacon.rssi_kalman,
                'dist': beacon.distance,
                'timestamp': beacon.timestamp.strftime('%H:%M:%S.%f')[:-3]
            }

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        with open(f'{self.output_dir}/{self.etude_name}.json', 'a') as f:
            json.dump(data, f)
            f.write('\n')
