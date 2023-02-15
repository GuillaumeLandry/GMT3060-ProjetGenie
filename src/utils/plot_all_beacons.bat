@echo off

if "%1"=="" (
    echo Donner en argument le nom de l'etude pour laquelle produire les graphiques
    echo Usage: plot_all_beacons.bat nom_fichier_sans_extension
    exit /b 1
)

start /B python data_plotter.py --etude %1 --beacon 1
start /B python data_plotter.py --etude %1 --beacon 2
start /B python data_plotter.py --etude %1 --beacon 3
start /B python data_plotter.py --etude %1 --beacon 4
start /B python data_plotter.py --etude %1 --beacon 5
start /B python data_plotter.py --etude %1 --beacon 6

echo Toutes les fenetres graphiques vont s'ouvrir dans un instant ...