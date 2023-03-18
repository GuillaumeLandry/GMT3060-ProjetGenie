import os
import json
import argparse
import pathlib, webbrowser

import plotly.graph_objects as go
import plotly.io as pio

class StudyPlotter:
    def __init__(self, etude_name):
        # Nom de l'étude à analyser
        self.etude_name = etude_name
        self.etude_directory = ''
        self.stats_figures = []

        # Données de l'étude
        self.timestamps_affichage = []
        self.timestamps = []
        self.positionsX = []
        self.positionsY = []
        self.errors = []

        # Variables utilisées dans la production des graphiques
        self.mapX = []
        self.mapY = []
        self.dangerX = []
        self.dangerY = []
        self.groundTruthX = []
        self.groundTruthY = []
        self.min_RSSI = float('inf')  # Initialise au float maximum disponible
        self.max_RSSI = float('-inf') # Initialise au float minimum disponible
        self.min_dist = float('inf')  # Initialise au float maximum disponible
        self.max_dist = float('-inf') # Initialise au float minimum disponible

        # Données des balises
        self.beacons = {1: {"dist": [], "rssi": [], "rssi_kalman": []},
                        2: {"dist": [], "rssi": [], "rssi_kalman": []},
                        3: {"dist": [], "rssi": [], "rssi_kalman": []},
                        4: {"dist": [], "rssi": [], "rssi_kalman": []},
                        5: {"dist": [], "rssi": [], "rssi_kalman": []},
                        6: {"dist": [], "rssi": [], "rssi_kalman": []}}
         
    def process_plots(self):
        # Toute la chaine de traitement pour produire les graphiques
        self.load_study()
        self.create_plots()
        self.export_telemetry()
        self.export_trajectory()

    def load_study(self):
        self.reset()

        # Détermine le chemin relatif à utiliser pour trouver l'étude
        if os.path.exists(f'./etudes/{self.etude_name}/{self.etude_name}.json'):
            self.etude_directory = f'./etudes/{self.etude_name}'
            self.carto_directory = f'./cartographies'
        elif os.path.exists(f'../etudes/{self.etude_name}/{self.etude_name}.json'):
            self.etude_directory = f'../etudes/{self.etude_name}'
            self.carto_directory = f'../cartographies'
        else:
            print("Aucune étude trouvée. Vérifier le nom de l'étude et/ou la position du fichier StudyPlotter.py")
            return
        
        # Charge les données d'acquisition dans les différents attributs de la classe
        with open(f'{self.etude_directory}/{self.etude_name}.json', 'r') as f:
            for line in f:
                obj = json.loads(line)

                self.timestamps.append(obj['timestamp'])
                self.positionsX.append(obj['position']['x'])
                self.positionsY.append(obj['position']['y'])
                self.errors.append(float(obj['position']['error']))

                for i in range(1, 7):
                    # S'il existe une distance calculée pour cette balise (donnée reçue)
                    if obj['beacons'][str(i)]['dist'] is not None:
                        self.beacons[i]['dist'].append(float(obj['beacons'][str(i)]['dist']))
                        self.beacons[i]['rssi'].append(float(obj['beacons'][str(i)]['rssi']))
                        self.beacons[i]['rssi_kalman'].append(float(obj['beacons'][str(i)]['rssi_kalman']))
                        
                        # Ajuste les valeurs de min et max RSSI pour ajuste l'échelle des graphiques sur l'axe des Y
                        if (float(obj['beacons'][str(i)]['rssi']) < self.min_RSSI): self.min_RSSI = float(obj['beacons'][str(i)]['rssi'])
                        if (float(obj['beacons'][str(i)]['rssi']) > self.max_RSSI): self.max_RSSI = float(obj['beacons'][str(i)]['rssi'])
                        if (float(obj['beacons'][str(i)]['dist']) < self.min_dist): self.min_dist = float(obj['beacons'][str(i)]['dist'])
                        if (float(obj['beacons'][str(i)]['dist']) > self.max_dist): self.max_dist = float(obj['beacons'][str(i)]['dist'])
                    
                    # Si aucune distance calculée (donnée non-reçue)
                    else:
                        self.beacons[i]['dist'].append(obj['beacons'][str(i)]['dist'])
                        self.beacons[i]['rssi'].append(obj['beacons'][str(i)]['rssi'])
                        self.beacons[i]['rssi_kalman'].append(obj['beacons'][str(i)]['rssi_kalman'])
        
        self.format_timestamps_affichage()

        # Charge la carte pour affichage dans le graphique de trajectoire
        with open(f'{self.carto_directory}/carte_lab.txt', 'r') as f:
            for line in f.readlines():
                x, y, z = line.strip().split(",")[1:4]
                self.mapX.append(float(x))
                self.mapY.append(float(y))

        # Charge la zone de danger pour affichage dans le graphique de trajectoire
        with open(f'{self.carto_directory}/carte_danger.txt', 'r') as f:
            for line in f.readlines():
                x, y, z = line.strip().split(",")[1:4]
                self.dangerX.append(float(x))
                self.dangerY.append(float(y))

        # Charge les données de la station-totale de cette étude
        try:
            with open(f'{self.etude_directory}/{self.etude_name}_Ground_Truth.txt', 'r') as f:
                for line in f.readlines():
                    x, y = line.strip().split(",")[0:2]
                    self.groundTruthX.append(float(x))
                    self.groundTruthY.append(float(y))
        except:
            # Crée un fichier vide si aucun n'existe (aucune donnée de station totale fournie)
            with open(f'{self.etude_directory}/{self.etude_name}_Ground_Truth.txt', 'w') as f:
                pass

    def create_plots(self):
        # RSSI Brut
        rssi_plots = []
        for i in range(1,7):
            rssi_plots.append(go.Scatter(name=f'B{i}', x=self.timestamps_affichage, y=self.beacons[i]['rssi'], mode='lines+markers'))
        figure_rssi = go.Figure(data=rssi_plots)
        figure_rssi.update_layout(
            title='RSSI Brut',
            title_x=0.5,
            xaxis_title='Temps écoulé (s)',
            yaxis_title='RSSI (dbm)',
            yaxis_range=[self.min_RSSI, self.max_RSSI]
        )

        # RSSI Kalman
        kalman_plots = []
        for i in range(1,7):
            kalman_plots.append(go.Scatter(name=f'B{i}_kalman', x=self.timestamps_affichage, y=self.beacons[i]['rssi_kalman'], mode='lines+markers'))
        figure_kalman = go.Figure(data=kalman_plots)
        figure_kalman.update_layout(
            title='RSSI Kalman',
            title_x=0.5,
            xaxis_title='Temps écoulé (s)',
            yaxis_title='RSSI (dbm)',
            yaxis_range=[self.min_RSSI, self.max_RSSI]
        )

        # RSSI Combiné (Brut + Kalman)
        figure_combine = go.Figure(data=rssi_plots + kalman_plots)
        figure_combine.update_layout(
            title='RSSI Combine (Brut + Kalman)',
            title_x=0.5,
            xaxis_title='Temps écoulé (s)',
            yaxis_title='RSSI (dbm)',
            yaxis_range=[self.min_RSSI, self.max_RSSI]
        )

        # Distances
        dist_plots = []
        for i in range(1,7):
            dist_plots.append(go.Scatter(name=f'B{i}', x=self.timestamps_affichage, y=self.beacons[i]['dist'], mode='lines+markers'))
        figure_dist = go.Figure(data=dist_plots)
        figure_dist.update_layout(
            title='Distances',
            title_x=0.5,
            xaxis_title='Temps écoulé (s)',
            yaxis_title='Distances (m)',
            yaxis_range=[self.min_dist, self.max_dist]
        )

        # Erreurs
        plot_erreur = go.Scatter(name="Erreurs", x=self.timestamps_affichage, y=self.errors, mode='lines+markers')
        figure_erreur = go.Figure(data=[plot_erreur])
        figure_erreur.update_layout(
            title='Erreurs',
            title_x=0.5,
            xaxis_title='Temps écoulé (s)',
            yaxis_title='Erreurs (m)',
        )

        # Trajectoire
        plot_map = go.Scatter(name="Fond de Carte", x=self.mapX, y=self.mapY, mode='lines+markers', line=dict(color='gray'))
        plot_danger = go.Scatter(name="Danger", x=self.dangerX, y=self.dangerY, mode='lines+markers', line=dict(color='rgb(214, 39, 40)'))
        plot_trajectory = go.Scatter(name="Trajectoire", x=self.positionsX, y=self.positionsY, mode='lines+markers', line=dict(color='rgb(31, 119, 180)'))
        plot_ground_truth = go.Scatter(name="Station-Totale", x=self.groundTruthX, y=self.groundTruthY, mode='lines+markers', line=dict(color='rgb(44, 160, 44)'))
        figure_trajectory = go.Figure(data=[plot_trajectory, plot_ground_truth, plot_map, plot_danger])
        figure_trajectory.update_layout(
            title='Trajectoire',
            title_x=0.5,
            xaxis_title='Coordonnée X (m)',
            yaxis_title='Coordonnée Y (m)',
            xaxis_range=[min(self.mapY), max(self.mapY)],
            yaxis_range=[min(self.mapY), max(self.mapY)]
        )

        self.stats_figures = [figure_rssi, figure_kalman, figure_combine, figure_dist, figure_erreur, figure_trajectory]
    
    def export_telemetry(self):
        with open(f'{self.etude_directory}/{self.etude_name}_Telemetrie.html', 'w') as f: 
            f.write('<html>\n')
            f.write('<head>\n')
            f.write(f'<title>{self.etude_name}_Telemetrie</title>\n')
            f.write('<style>\n')
            f.write('body { font-family: Arial, Helvetica, sans-serif; }\n')
            f.write('h1 { text-align: center; font-size: 36px; margin-top: 50px; }\n')
            f.write('h2 { text-align: center; font-size: 24px; margin-top: 30px; }\n')
            f.write('.container { display: flex; flex-wrap: wrap; justify-content: space-between; margin-top: 50px; }\n')
            f.write('.plot-container { width: 48%; height: 500px; margin-bottom: 50px; }\n')
            f.write('.separator { border-top: 2px solid black; margin: 50px 0; }\n')
            f.write('</style>\n')
            f.write('</head>\n')
            f.write('<body>\n')
            f.write(f'<h1>Donnees de telemetrie et de traitements</h1>\n')
            f.write(f'<h2>Etude : {self.etude_name}</h2>\n')
            f.write(f'<h2>Debut : {self.timestamps[0][:-7]} | Fin : {self.timestamps[-1][:-7]} | Duree : {self.timestamps_affichage[-1]} s</h2>\n')
            f.write('<hr class="separator">\n')
            f.write('<div class="container">\n')
            for i, fig in enumerate(self.stats_figures):
                if fig.layout.title.text != "Trajectoire":
                    f.write(f'<div class="plot-container">\n')
                    #f.write(f'<h2 style="text-align:center;">Graphique {i+1} - {fig.layout.title.text}</h2>\n')
                    # Ajouter chaque figure au document .html
                    f.write(fig.to_html(include_plotlyjs='cdn'))
                    # Exporter chaque figure comme .png
                    pio.write_image(fig, file=f'{self.etude_directory}/{self.etude_name}_{fig.layout.title.text}.png', scale=4)
                    f.write('</div>\n')
            f.write('</div>\n')
            f.write('</body>\n')
            f.write('</html>\n')

        uri = pathlib.Path(f'{self.etude_directory}/{self.etude_name}_Telemetrie.html').absolute().as_uri()
        webbrowser.open(uri)

    def export_trajectory(self):
        with open(f'{self.etude_directory}/{self.etude_name}_Trajectoire.html', 'w') as f: 
            f.write('<html>\n')
            f.write('<head>\n')
            f.write(f'<title>{self.etude_name}_Trajectoire</title>\n')
            f.write('<style>\n')
            f.write('body { font-family: Arial, Helvetica, sans-serif; }\n')
            f.write('h1 { text-align: center; font-size: 36px; margin-top: 50px; }\n')
            f.write('h2 { text-align: center; font-size: 24px; margin-top: 30px; }\n')
            f.write('.container { display: flex; flex-wrap: wrap; justify-content: space-between; margin-top: 50px; }\n')
            f.write('.plot-container { width: 48%; height: 500px; margin-bottom: 50px; }\n')
            f.write('.separator { border-top: 2px solid black; margin: 50px 0; }\n')
            f.write('</style>\n')
            f.write('</head>\n')
            f.write('<body>\n')
            f.write(f'<h1>Trajectoire</h1>\n')
            f.write(f'<h2>Etude : {self.etude_name}</h2>\n')
            f.write(f'<h2>Debut : {self.timestamps[0][:-7]} | Fin : {self.timestamps[-1][:-7]} | Duree : {self.timestamps_affichage[-1]} s</h2>\n')
            f.write('<hr class="separator">\n')
            for i, fig in enumerate(self.stats_figures):
                if fig.layout.title.text == "Trajectoire":
                    f.write(fig.to_html(include_plotlyjs='cdn'))
            f.write('</div>\n')
            f.write('</body>\n')
            f.write('</html>\n')

        uri = pathlib.Path(f'{self.etude_directory}/{self.etude_name}_Trajectoire.html').absolute().as_uri()
        webbrowser.open(uri)

    def format_timestamps_affichage(self):
        # Passer de "YY-MM-DD HH:MM:SS.ssssss" à "HH:MM:SS.ss"
        self.timestamps_affichage = [ts.split(" ")[1][:12] for ts in self.timestamps]

        # Passer de "HH:MM:SS.ss" à "ssssss.ss" pour le premier timestamp
        ts_0 = sum([float(t) * 60 ** i for i, t in enumerate(self.timestamps_affichage[0].split(':')[::-1])])

        # Faire la différence entre les timestamps pour avoir le temps écoulé en format "ssssss.ss"
        self.timestamps_affichage = [round(sum([float(t) * 60 ** i for i, t in enumerate(ts.split(':')[::-1])]) - ts_0, 2) for ts in self.timestamps_affichage]

    def reset(self):
        self.stats_figures = []
        self.timestamps_affichage = []
        self.timestamps = []
        self.positionsX = []
        self.positionsY = []
        self.errors = []
        self.beacons = {1: {"dist": [], "rssi": [], "rssi_kalman": []},
                        2: {"dist": [], "rssi": [], "rssi_kalman": []},
                        3: {"dist": [], "rssi": [], "rssi_kalman": []},
                        4: {"dist": [], "rssi": [], "rssi_kalman": []},
                        5: {"dist": [], "rssi": [], "rssi_kalman": []},
                        6: {"dist": [], "rssi": [], "rssi_kalman": []}}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Comment utiliser le script: python StudyPlotter.py -e <nom_fichier_sans_extension>')
    parser.add_argument('-e', '--etude', type=str, help='Nom du fichier d\'étude à lire (sans son extension .json)')
    args = parser.parse_args()

    # Si aucun argument n'a été fourni, afficher l'aide
    if not args.etude:
        parser.print_help()
    else:    
        plotter = StudyPlotter(args.etude)
        plotter.process_plots()

