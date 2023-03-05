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
        self.export_plots()

    def load_study(self):
        self.reset()

        # Détermine le chemin relatif à utiliser pour trouver l'étude
        if os.path.exists(f'./etudes/{self.etude_name}/{self.etude_name}.json'):
            self.etude_directory = f'./etudes/{self.etude_name}'
        elif os.path.exists(f'../etudes/{self.etude_name}/{self.etude_name}.json'):
            self.etude_directory = f'../etudes/{self.etude_name}'
        else:
            print("Aucune étude trouvée. Vérifier le nom de l'étude et/ou la position du fichier StudyPlotter.py")
            return

        # Charge les données dans les différents attributs de la classe
        with open(f'{self.etude_directory}/{self.etude_name}.json', 'r') as f:
            for line in f:
                obj = json.loads(line)[0]

                self.timestamps.append(obj['timestamp'])
                self.positionsX.append(obj['position']['x'])
                self.positionsY.append(obj['position']['y'])
                self.errors.append(float(obj['position']['error']))

                for i in range(1, 7):
                    if obj['beacons'][str(i)]['dist'] is not None:
                        self.beacons[i]['dist'].append(float(obj['beacons'][str(i)]['dist']))
                        self.beacons[i]['rssi'].append(float(obj['beacons'][str(i)]['rssi']))
                        self.beacons[i]['rssi_kalman'].append(float(obj['beacons'][str(i)]['rssi_kalman']))
                    else:
                        self.beacons[i]['dist'].append(obj['beacons'][str(i)]['dist'])
                        self.beacons[i]['rssi'].append(obj['beacons'][str(i)]['rssi'])
                        self.beacons[i]['rssi_kalman'].append(obj['beacons'][str(i)]['rssi_kalman'])
        
        self.format_timestamps_affichage()

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
            yaxis_title='RSSI (dbm)'
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
            yaxis_title='RSSI (dbm)'
        )

        # RSSI Combiné (Brut + Kalman)
        figure_combine = go.Figure(data=rssi_plots + kalman_plots)
        figure_combine.update_layout(
            title='RSSI Combine (Brut + Kalman)',
            title_x=0.5,
            xaxis_title='Temps écoulé (s)',
            yaxis_title='RSSI (dbm)'
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
            yaxis_title='Distances (m)'
        )

        # Erreurs
        plot_erreur = go.Scatter(name="Erreurs", x=self.timestamps_affichage,y=self.errors,mode='lines+markers')
        figure_erreur = go.Figure(data=[plot_erreur])
        figure_erreur.update_layout(
            title='Erreurs',
            title_x=0.5,
            xaxis_title='Temps écoulé (s)',
            yaxis_title='Erreurs (m)'
        )

        # Positions
        plot_positions = go.Scatter(name="Positions", x=self.positionsX,y=self.positionsY,mode='lines+markers')
        figure_position = go.Figure(data=[plot_positions])
        figure_position.update_layout(
            title='Positions',
            title_x=0.5,
            xaxis_title='Coordonnée X (m)',
            yaxis_title='Coordonnée Y (m)'
        )

        self.stats_figures = [figure_rssi, figure_kalman, figure_combine, figure_dist, figure_erreur, figure_position]

    def export_plots(self):
        with open(f'{self.etude_directory}/{self.etude_name}.html', 'w') as f: 
            f.write('<html>\n')
            f.write('<head>\n')
            f.write(f'<title>{self.etude_name}</title>\n')
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
                f.write(f'<div class="plot-container">\n')
                #f.write(f'<h2 style="text-align:center;">Graphique {i+1} - {fig.layout.title.text}</h2>\n')
                f.write(fig.to_html(include_plotlyjs='cdn'))
                f.write('</div>\n')
            f.write('</div>\n')
            f.write('</body>\n')
            f.write('</html>\n')

        uri = pathlib.Path(f'{self.etude_directory}/{self.etude_name}.html').absolute().as_uri()
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

