#Permet de monter le gluster
sudo mount.glusterfs pi2:/testvol /mnt/glusterfs
sudo mount

#Permet de lancer le serveur de telechargement, pour le master
sudo node /home/pi/Documents/docker-task-builder/serveur.js