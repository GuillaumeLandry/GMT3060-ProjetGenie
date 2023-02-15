import matplotlib.pyplot as plt
import datetime
import json
import argparse

class DataPlotter:
    def __init__(self, etude_name, beacon_name):
        self.etude_name = etude_name
        self.beacon_name = beacon_name
        self.distances = []
        self.rssis = []
        self.timestamps = []
        self.positions = []
        self.errors = []

        self.load_data()
        self.plot_data()

    def load_data(self):
        self.reset()
        with open(f'../etudes/{self.etude_name}.json', 'r') as f:
            for line in f:
                obj = json.loads(line)[0]
                self.timestamps.append(obj['timestamp'])
                self.positions.append(obj['position'])
                self.errors.append(obj['position']['error'])
                self.distances.append(obj['beacons'][self.beacon_name]['dist'])
                self.rssis.append(obj['beacons'][self.beacon_name]['rssi'])

    def plot_data(self):
        # Convert dates to datetime objects
        dates = [datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in self.timestamps]

        # Create a figure and axis
        fig, axs = plt.subplots(nrows=2, ncols=2)
        fig.suptitle(f'Données de télémétrie et de traitements de la balise {self.beacon_name} pendant l\'étude "{self.etude_name}"')

        # GRAPH 1
        axs[0, 0].set_title('Variations de RSSI')
        axs[0, 0].set_xlabel('Temps')
        axs[0, 0].set_xticklabels([])
        axs[0, 0].set_ylabel('RSSI (dBm)')
        axs[0, 0].plot(dates, self.rssis)

        # GRAPH 2
        axs[0, 1].set_title('Variations de distances')
        axs[0, 1].set_xlabel('Temps')
        axs[0, 1].set_xticklabels([])
        axs[0, 1].set_ylabel('Distances (m)')
        axs[0, 1].plot(dates, self.distances)

        # GRAPH 3
        axs[1, 0].set_title('Variations des erreurs')
        axs[1, 0].set_xlabel('Temps')
        axs[1, 0].set_xticklabels([])
        axs[1, 0].set_ylabel('Erreurs (m)')
        axs[1, 0].plot(dates, self.errors)

        # Display the plot
        plt.show()

    def reset(self):
        self.distances = []
        self.rssis = []
        self.timestamps = []
        self.positions = []
        self.errors = []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Utiliser le script: python data_plotter.py --etude <nom_fichier_sans_extension> --beacon <nom_beacon')
    parser.add_argument('--etude', type=str, help='Nom du fichier d\'étude à lire')
    parser.add_argument('--beacon', type=str, help='Nom (numéro) du beacon pour lequel afficher les données')

    args = parser.parse_args()

    plotter = DataPlotter(args.etude, args.beacon)
