# Introduction

Ce dépot contient le front-end de notre projet SI réutilisant node-red.

Ce projet consiste à réaliser une interface permettant de réaliser un schéma.

Ce schéma représentera un enchainement de traitements vidéos utilisant des conteneurs Docker.

Cet enchainement sera alors exporté au format JSON puis envoyé à un ensemble de RasberyPI chargé d'executer le traitement.

# Lignes de commandes

* Construire l'image à partir du Dockerfile : 
```
docker build -t iprocessbuilder .
```

* Lancer le conteneur de l'image "iprocessbuilder" : 
```
docker run -d -p 1880:1880 --name cprocessbuilder iprocessbuilder
```

* Arreter le conteneur "cprocessbuilder" : 
```
docker stop cprocessbuilder
```

* Relancer le conteneur "cprocessbuilder" : 
```
docker start cprocessbuilder
```