# Projet de positionnement intérieur

## Mise en contexte
Ce répertoire comprend toute l'architecture technologique développée dans le cadre du projet de positionnement intérieur. Les outils développés permettent de :

1. Acquérir des données bluetooth provenant de balises BLE avec un appareil Android (récepteur) à l'aide d'une application native; 
1. Transmettre les données à un serveur local fonctionnant sur un ordinateur de contrôle;
1. Traiter les données pour calculer la distance récepteur-balises et la position du récepteur;
1. Afficher en temps-réel les données et résultats dans une interface web;

Voici le schéma de l'architecture développée:
![Architecture](./assets/architecture.png)

## Utiliser le projet
1. Cloner le répertoire du projet avec git
```bash
git clone https://github.com/GuillaumeLandry/GMT3060-ProjetGenie.git
```

2. Installer la dernière version de l'application Android sur l'appareil qui servira de récepteur (Voir comment installer un ".apk" sur ce [site web](https://www.groovypost.com/howto/install-apk-files-on-android/))
```bash
# Répertoire des fichiers .apk
src/Android/APKs/Release <date-la-plus-récente>/
```

3. Installer les dépendances python nécessaires pour le serveur, les calculs et l'affichage
```bash
pip install -r requirements.txt
```

4. Lancer le serveur de positionnement
```bash
cd src
python server_launcher.py
```

5. Dans l'application Android, aller dans l'onglet "Settings" et modifier l'URL pour celui qui est affiché dans la console lors du démarrage du serveur.

## Ressources
* [BLE Guide](https://punchthrough.com/android-ble-guide/)
* [BLE Youtube Series](https://www.youtube.com/watch?v=eZGixQzBo7Y)

* [Python bluetooth scanning](https://geektechstuff.com/2020/06/01/python-and-bluetooth-part-1-scanning-for-devices-and-services-python/)
* [Android connectivity samples](https://github.com/android/connectivity-samples/tree/master)
* [Estimote Packet Specs](https://github.com/Estimote/estimote-specs)
* [Estimote Telemetry](https://developer.estimote.com/sensors/estimote-telemetry/)