# Introduction

Ce dépot contient le front-end de notre projet SI réutilisant node-red.

Ce projet consiste à réaliser une interface permettant de réaliser un schéma.

Ce schéma représentera un enchainement de traitements vidéos utilisant des conteneurs Docker.

Cet enchainement sera alors exporté au format JSON puis envoyé à un ensemble de RasberyPI chargé d'executer le traitement.

# Lignes de commandes

* Construire l'image à partir du Dockerfile : 
```
docker build -t processbuilder .
```

* Lancer l'image du conteneur "processbuilder" : 
```
docker run -it -p 1880:1880 --name iprocessbuilder processbuilder
```