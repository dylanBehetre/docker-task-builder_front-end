#!/usr/bin/python


import subprocess
import time
import sqlite3

def isCompleted(task):
    result = subprocess.getstatusoutput("docker service ps "+task+" | sed -n 2p | sed -E \"s/[[:space:]]+/ /g\" | cut -f6 -d' '")[1]
    if result == "Complete":
        return True
    return False





#chercher toutes les tâches pour un uuid
def getStatusTasks(uuid):
    tasks = subprocess.getstatusoutput("docker service ls | sed -n 1!p | sed -E \"s/[[:space:]]+/ /g\" | cut -f2 -d ' ' | grep "+uuid+"")[1]
    tasks = tasks.split('\n')
    nb_tasks = len(tasks)
    nb_complete = 0
    for task in tasks:
        if isCompleted(task):
            nb_complete = nb_complete + 1

    if nb_complete is nb_tasks:
        print("on peut merge les tâches dont l'uui est "+uuid)
        for task in tasks:
            subprocess.call(["docker", "service", "rm", task])
        with sqlite3.connect('bdd/provisioning.db') as DBconn:
            c = DBconn.cursor()
            #on a juste l'uuid mais on sait pas de quel table il vient, on suppr dans les 2
            try:
                c.execute("DELETE FROM priority WHERE uuid=?",(uuid,))
                c.execute("DELETE FROM normal WHERE uuid=?",(uuid,))
        DBconn.close()
        #Faut merger les fichier qui commencent par uuid
        #pour ça on check avant de supprimer les services qui commencent par uuid_z et on récup les filtres / fichiers



while True:
    list_services = subprocess.getstatusoutput("docker service ls | sed -n 1!p | sed -E \"s/[[:space:]]+/ /g\" | cut -f2 -d ' '| cut -f1 -d '_' | sort -u")[1]
    list_services = list_services.split('\n')

    for services in list_services:
        getStatusTasks(services)
    time.sleep(5)
