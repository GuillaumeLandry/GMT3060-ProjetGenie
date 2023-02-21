import os
import json
import argparse
import pathlib, webbrowser

import plotly.graph_objects as go
import plotly.io as pio

class DataPlotter:
    def __init__(self, etude_name):
        # Nom de l'étude à analyser
        self.etude_name = etude_name

        # Données de l'étude
        self.timestamps_affichage = []
        self.timestamps = []
        self.positionsX = []
        self.positionsY = []
        self.errors = []

        # Données des balises
        self.B1_dist = []
        self.B1_rssi = []
        self.B2_dist = []
        self.B2_rssi = []
        self.B3_dist = []
        self.B3_rssi = []
        self.B4_dist = []
        self.B4_rssi = []
        self.B5_dist = []
        self.B5_rssi = []
        self.B6_dist = []
        self.B6_rssi = []

    def load_data(self):
        self.reset()
        with open(f'./etudes/{self.etude_name}/{self.etude_name}.json', 'r') as f:
            for line in f:
                obj = json.loads(line)[0]

                self.timestamps.append(obj['timestamp'])
                self.positionsX.append(obj['position']['x'])
                self.positionsY.append(obj['position']['y'])
                self.errors.append(float(obj['position']['error']))

                # Balise 1
                if self.check_valid(obj['beacons']['1']):
                    self.B1_dist.append(float(obj['beacons']['1']['dist']))
                    self.B1_rssi.append(float(obj['beacons']['1']['rssi']))
                else:
                    self.B1_dist.append(obj['beacons']['1']['dist'])
                    self.B1_rssi.append(obj['beacons']['1']['rssi'])

                # Balise 2
                if self.check_valid(obj['beacons']['2']):
                    self.B2_dist.append(float(obj['beacons']['2']['dist']))
                    self.B2_rssi.append(float(obj['beacons']['2']['rssi']))
                else:
                    self.B2_dist.append(obj['beacons']['2']['dist'])
                    self.B2_rssi.append(obj['beacons']['2']['rssi'])
                
                # Balise 3
                if self.check_valid(obj['beacons']['3']):
                    self.B3_dist.append(float(obj['beacons']['3']['dist']))
                    self.B3_rssi.append(float(obj['beacons']['3']['rssi']))
                else:
                    self.B3_dist.append(obj['beacons']['3']['dist'])
                    self.B3_rssi.append(obj['beacons']['3']['rssi'])

                # Balise 4
                if self.check_valid(obj['beacons']['4']):
                    self.B4_dist.append(float(obj['beacons']['4']['dist']))
                    self.B4_rssi.append(float(obj['beacons']['4']['rssi']))
                else:
                    self.B4_dist.append(obj['beacons']['4']['dist'])
                    self.B4_rssi.append(obj['beacons']['4']['rssi'])

                # Balise 5
                if self.check_valid(obj['beacons']['5']):
                    self.B5_dist.append(float(obj['beacons']['5']['dist']))
                    self.B5_rssi.append(float(obj['beacons']['5']['rssi']))
                else:
                    self.B5_dist.append(obj['beacons']['5']['dist'])
                    self.B5_rssi.append(obj['beacons']['5']['rssi'])
                
                # Balise 6
                if self.check_valid(obj['beacons']['6']):
                    self.B6_dist.append(float(obj['beacons']['6']['dist']))
                    self.B6_rssi.append(float(obj['beacons']['6']['rssi']))
                else:
                    self.B6_dist.append(obj['beacons']['6']['dist'])
                    self.B6_rssi.append(obj['beacons']['6']['rssi'])
        
        self.format_timestamps_affichage()
                    
    def create_and_export_stats(self):
        self.load_data()
        figures = self.create_stats()
        self.export_stats(figures)

    def create_stats(self):

        # RSSI
        B1_plot_rssi = go.Scatter(name="B1", x=self.timestamps_affichage,y=self.B1_rssi,mode='lines+markers')
        B2_plot_rssi = go.Scatter(name="B2", x=self.timestamps_affichage,y=self.B2_rssi,mode='lines+markers',visible='legendonly')
        B3_plot_rssi = go.Scatter(name="B3", x=self.timestamps_affichage,y=self.B3_rssi,mode='lines+markers',visible='legendonly')
        B4_plot_rssi = go.Scatter(name="B4", x=self.timestamps_affichage,y=self.B4_rssi,mode='lines+markers',visible='legendonly')
        B5_plot_rssi = go.Scatter(name="B5", x=self.timestamps_affichage,y=self.B5_rssi,mode='lines+markers',visible='legendonly')
        B6_plot_rssi = go.Scatter(name="B6", x=self.timestamps_affichage,y=self.B6_rssi,mode='lines+markers',visible='legendonly')
        figure_rssi = go.Figure(data=[B1_plot_rssi, B2_plot_rssi, B3_plot_rssi, B4_plot_rssi, B5_plot_rssi, B6_plot_rssi])
        figure_rssi.update_layout(
            title='RSSI',
            title_x=0.5,
            xaxis_title='Temps écoulé (s)',
            yaxis_title='RSSI (dbm)'
        )

        # Distances
        B1_plot_dist = go.Scatter(name="B1", x=self.timestamps_affichage,y=self.B1_dist,mode='lines+markers')
        B2_plot_dist = go.Scatter(name="B2", x=self.timestamps_affichage,y=self.B2_dist,mode='lines+markers',visible='legendonly')
        B3_plot_dist = go.Scatter(name="B3", x=self.timestamps_affichage,y=self.B3_dist,mode='lines+markers',visible='legendonly')
        B4_plot_dist = go.Scatter(name="B4", x=self.timestamps_affichage,y=self.B4_dist,mode='lines+markers',visible='legendonly')
        B5_plot_dist = go.Scatter(name="B5", x=self.timestamps_affichage,y=self.B5_dist,mode='lines+markers',visible='legendonly')
        B6_plot_dist = go.Scatter(name="B6", x=self.timestamps_affichage,y=self.B6_dist,mode='lines+markers',visible='legendonly')
        figure_dist = go.Figure(data=[B1_plot_dist, B2_plot_dist, B3_plot_dist, B4_plot_dist, B5_plot_dist, B6_plot_dist])
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

        return [figure_rssi, figure_dist, figure_erreur, figure_position]

    def export_stats(self, figures):
        output_dir = f'./etudes/{self.etude_name}'
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(f'{output_dir}/{self.etude_name}.html', 'w') as f:
            f.write(f'<h1 style="text-align: center;">Donnees de telemetrie et de traitements<br></h1>'
                    f'<h2 style="text-align: center; justify"><div style="display: inline-block; text-align: left;">'
                    f'Etude : {self.etude_name}<br>'
                    f'Debut : {self.timestamps[0][:-7]}<br>'
                    f'Fin   : {self.timestamps[-1][:-7]}<br>'
                    f'Duree : {self.timestamps_affichage[-1]} s</h2></div>')
            f.write(figures[0].to_html(include_plotlyjs='cdn'))
            pio.write_image(figures[0], file=f'{output_dir}/{self.etude_name}_{figures[0].layout.title.text}.png', scale=4)
            
            for fig in figures[1:]:
                f.write(fig.to_html(full_html=False, include_plotlyjs=False))
                pio.write_image(fig, file=f'{output_dir}/{self.etude_name}_{fig.layout.title.text}.png', scale=4)
            
        uri = pathlib.Path(f'{output_dir}/{self.etude_name}.html').absolute().as_uri()
        webbrowser.open(uri)
    
    def format_timestamps_affichage(self):
        # Passer de "YY-MM-DD HH:MM:SS.ssssss" à "HH:MM:SS.ss"
        for ts in self.timestamps:
            self.timestamps_affichage.append(ts.split(" ")[1][:-4])

        # Passer de "HH:MM:SS.ss" à "ssssss.ss" pour le premier timestamp
        hhmmss0 = self.timestamps_affichage[0].split(':')
        ts_0 = float(hhmmss0[0])*3600 + float(hhmmss0[1])*60 + float(hhmmss0[2])

        # Faire la différence entre les timestamps pour avoir le temps écoulé en format "ssssss.ss"
        for idx, ts in enumerate(self.timestamps_affichage):
            hhmmss = ts.split(':')
            ts_i = float(hhmmss[0])*3600 + float(hhmmss[1])*60 + float(hhmmss[2])
            self.timestamps_affichage[idx] = round(ts_i - ts_0, 2)
    
    def check_valid(self, beacon_data):
        return beacon_data['dist'] != None

    def reset(self):
        self.timestamps_affichage = []

        self.timestamps = []
        self.positionsX = []
        self.positionsY = []
        self.errors = []

        self.B1_dist = []
        self.B1_rssi = []
        self.B2_dist = []
        self.B2_rssi = []
        self.B3_dist = []
        self.B3_rssi = []
        self.B4_dist = []
        self.B4_rssi = []
        self.B5_dist = []
        self.B5_rssi = []
        self.B6_dist = []
        self.B6_rssi = []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Comment utiliser le script: python plot_study.py -e <nom_fichier_sans_extension>')
    parser.add_argument('-e', '--etude', type=str, help='Nom du fichier d\'étude à lire (sans son extension .json)')
    args = parser.parse_args()

    # If no arguments were provided, show help
    if not args.etude:
        parser.print_help()
    else:    
        plotter = DataPlotter(args.etude)
        plotter.create_and_export_stats()

