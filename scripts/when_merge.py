#!/usr/bin/python


import subprocess
import time
import sqlite3


'''
Author : Antoine-Adrien Parent

Ce script a pour but de merger les fichiers dont les traitements sont finis.

Pour toutes questions : antoineparent@hotmail.fr
'''

#Le chemin vers le fichier .db
pathToDatabase = '/mnt/glusterfs/bdd/provisioning.db'


#Vérifie qu'une tache est terminée
def isCompleted(task):
    result = subprocess.getstatusoutput("docker service ps "+task+" | sed -n 2p | sed -E \"s/[[:space:]]+/ /g\" | cut -f6 -d' '")[1]
    if result == "Complete":
        return True
    return False


#chercher toutes les tâches pour un uuid
def try_to_remove_task(uuid):
    tasks = subprocess.getstatusoutput("docker service ls | sed -n 1!p | sed -E \"s/[[:space:]]+/ /g\" | cut -f2 -d ' ' | grep "+uuid+"")[1]
    tasks = tasks.split('\n')
    nb_tasks = len(tasks)
    nb_complete = 0
    for task in tasks:
        if isCompleted(task):
            nb_complete = nb_complete + 1

    #si toutes les tâches sont finies
    if nb_complete is nb_tasks:
        print("on peut merge les tâches dont l'uuid est "+uuid)
        print("la commande du merge")
        for task in tasks:
            subprocess.call(["docker", "service", "rm", task])
        with sqlite3.connect(pathToDatabase) as DBconn:
            c = DBconn.cursor()
            #on a juste l'uuid mais on sait pas de quel table il vient, on suppr dans les 2
            try:
                c.execute("DELETE FROM priority WHERE uuid=?",(uuid,))
                c.execute("DELETE FROM normal WHERE uuid=?",(uuid,))
            finally:
                DBconn.close()
        #Faut merger les fichier qui commencent par uuid
        #pour ça on check avant de supprimer les services qui commencent par uuid_z et on récup les filtres / fichiers



while True:
    list_services = subprocess.getstatusoutput("docker service ls | sed -n 1!p | sed -E \"s/[[:space:]]+/ /g\" | cut -f2 -d ' '| cut -f1 -d '_' | sort -u")[1]
    list_services = list_services.split('\n')

    for services in list_services:
        print(services)
        try_to_remove_task(services)
    time.sleep(5)
