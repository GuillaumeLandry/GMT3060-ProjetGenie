import matplotlib.pyplot as plt
import json
import argparse
import os

class DataPlotter:
    def __init__(self, etude_name, beacon_name, flag_all):
        self.etude_name = etude_name
        self.beacon_name = beacon_name
        self.distances = []
        self.rssis = []
        self.timestamps = []
        self.positionsX = []
        self.positionsY = []
        self.errors = []

        if (flag_all == True):
            self.load_and_plot_all()
        else: 
            self.load_data()
            self.plot_data()

    def load_data(self):
        self.reset()
        with open(f'../etudes/{self.etude_name}.json', 'r') as f:
            for line in f:
                obj = json.loads(line)[0]

                if obj['beacons'][self.beacon_name]['dist'] is not None:
                    self.timestamps.append(self.format_timestamp(obj['timestamp']))
                    self.positionsX.append(obj['position']['x']) ## TODO NON FONCTIONNEL
                    self.positionsY.append(obj['position']['y']) ## TODO NON FONCTIONNEL
                    self.errors.append(float(obj['position']['error']))
                    self.distances.append(float(obj['beacons'][self.beacon_name]['dist']))
                    self.rssis.append(float(obj['beacons'][self.beacon_name]['rssi']))
        
        self.prepare_timestamps_affichage()

    def plot_data(self):
        # Create a figure and axis
        fig, axs = plt.subplots(nrows=2, ncols=2)
        fig.suptitle(f'Données de télémétrie et de traitements de la balise {self.beacon_name} pendant l\'étude "{self.etude_name}"')
        fig.subplots_adjust(hspace=0.6)

        # GRAPH 1
        axs[0, 0].set_title('RSSI')
        axs[0, 0].set_xlabel('Temps (s)')
        axs[0, 0].set_xticklabels(self.ts_affichage, rotation=45)
        axs[0, 0].set_ylabel('RSSI (dBm)')
        axs[0, 0].plot(self.ts_affichage, self.rssis)

        # GRAPH 2
        axs[0, 1].set_title('Distances')
        axs[0, 1].set_xlabel('Temps (s)')
        axs[0, 1].set_xticklabels(self.ts_affichage, rotation=45)
        axs[0, 1].set_ylabel('Distances (m)')
        axs[0, 1].plot(self.ts_affichage, self.distances)

        # GRAPH 3
        axs[1, 0].set_title('Erreurs')
        axs[1, 0].set_xlabel('Temps (s)')
        axs[1, 0].set_xticklabels(self.ts_affichage, rotation=45)
        axs[1, 0].set_ylabel('Erreurs (m)')
        axs[1, 0].plot(self.ts_affichage, self.errors)

        # GRAPH 4
        axs[1, 1].set_title('Positions')
        axs[1, 1].set_xlabel('Coordonnées X (m)')
        ##axs[1, 0].set_xticklabels(self.positionsX, rotation=45)
        axs[1, 1].set_ylabel('Coordonnées Y (m)')
        axs[1, 1].plot(self.positionsX, self.positionsY)

        # Display the plot
        if not os.path.exists(f'../etudes/Figures_{self.etude_name}'):
            os.makedirs(f'../etudes/Figures_{self.etude_name}')
        plt.savefig(f'../etudes/Figures_{self.etude_name}/{self.etude_name}_B{self.beacon_name}.png')
        plt.show()

    def reset(self):
        self.distances = []
        self.rssis = []
        self.timestamps = []
        self.positionsX = []
        self.positionsY = []
        self.errors = []
        self.ts_affichage = []

    def format_timestamp(self, timestamp):
        return timestamp.split(" ")[1][:-4]
    
    def prepare_timestamps_affichage(self):
        self.ts_affichage = []

        hhmmss0 = self.timestamps[0].split(':')
        ts_0 = float(hhmmss0[0])*3600 + float(hhmmss0[1])*60 + float(hhmmss0[2])

        for ts in self.timestamps:
            hhmmss = ts.split(':')
            ts_i = float(hhmmss[0])*3600 + float(hhmmss[1])*60 + float(hhmmss[2])
            self.ts_affichage.append(round(ts_i - ts_0, 2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Comment utiliser le script: python data_plotter.py -e <nom_fichier_sans_extension> -b <nom_beacon')
    parser.add_argument('-e', '--etude', type=str, help='Nom du fichier d\'étude à lire (sans son extension .json)')
    parser.add_argument('-b', '--beacon', type=str, default='', help='Nom (numéro) de la balise pour laquelle afficher les données')
    parser.add_argument('-a', '--all', default=False, action='store_true', help='Affiche les donées de toutes les balises dans des graphiques conjoints')

    args = parser.parse_args()

    plotter = DataPlotter(args.etude, args.beacon, args.all)
