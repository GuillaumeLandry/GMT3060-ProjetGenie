@echo off

start /B python data_plotter.py --etude %1 --beacon 1
start /B python data_plotter.py --etude %1 --beacon 2
start /B python data_plotter.py --etude %1 --beacon 3
start /B python data_plotter.py --etude %1 --beacon 4
start /B python data_plotter.py --etude %1 --beacon 5
start /B python data_plotter.py --etude %1 --beacon 6

echo Toutes les fenetres graphiques vont s'ouvrir dans un instant ...