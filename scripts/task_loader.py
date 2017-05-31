#!/usr/bin/python

import sqlite3
import json
import subprocess
import os.path
import time
import re

'''
Author : Antoine-Adrien Parent

Ce script a pour but de lancer les tâches stockées en BDD.
Il va aller chercher en BDD les tâches prioritaires s'il y en a, sinon il ira chercher les tâches non-prioritaires.

Pour toutes questions : antoineparent@hotmail.fr
'''

#Sert à vérifier en BDD si la table "priority" est vide ou non.
#Return True si la table est vide.
def checkIfPrioEmpty():
    with sqlite3.connect('/mnt/glusterfs/bdd/provisioning.db') as DBconn:
        c = DBconn.cursor()
        c.execute("SELECT MAX(order_queue) FROM priority;")
        position = c.fetchone()[0]
    DBconn.close()
    if position is None:
        return True
    else:
        return False

#Sert à lancer la commande ffprobe et attendre qu'elle se termine.
#La fonction récupère l'output de ffprobe et le return
def ffprobeToJson(theFile):
    json = subprocess.check_output(
        'ffprobe -v quiet -print_format json -show_format -show_streams %s ' %theFile,
        stderr=subprocess.STDOUT,
        shell=True)
    return json

#Return le champ "streams" du JSON récupéré avec ffprobe
def streamsData(pythonJson):
    streams = pythonJson['streams']
    return streams

#Convertie l'output de ffprobe en JSON
def jsonToPython(theJson):
    return json.loads(theJson)

#Sert à vérifier qu'une tâche s'est bien terminée
def isCompleted(task):
    result = subprocess.getstatusoutput("docker service ps "+task+" | sed -n 2p | sed -E \"s/[[:space:]]+/ /g\" | cut -f6 -d' '")[1]
    if result == "Complete":
        return True
    return False

#Sert à savoir si un chemin est du type /zrezij/dapo/zpo ou C:\zefzef\htfgfr\zsdz
#Return True si c'est un chemin de type unix /zerzer/efzfe/lpl
def isUnixPath(path):
    pattern = re.compile("^\/$|(^(?=\/)|^\.|^\.\.)(\/(?=[^/\0])[^/\0]+)*\/?$")
    result = pattern.match(path)
    if result:
        return True
    return False

#On donne un path de type unix et on récupère le nom de fichier
def getUnixFilename(path):
    result = path
    result = result[::-1] #on met retourne la string à l'envers
    result = result.split("\/") #on split pour enlever les /
    result = result[0][::-1] #on remet le nom du fichier à l'endroit
    return result

#On donne un path de type windows et on récupère le nom de fichier
def getWindowsFilename(path):
    result = path
    result = result[::-1] #on met retourne la string à l'envers
    result = result.split("\\") #on split pour enlever les \
    result = result[0][::-1] #on remet le nom du fichier à l'endroit
    return result

#Permet de compter le nombre de canaux audio
def countAudioStream(stream):
    cpt = 0
    for i in stream:
        if (i['codec_type'] == "audio"):
            cpt = cpt + 1
    return cpt

#Permet de générer les paramètres pour la vitesse du son
def genSpeedParam(nb_codec, vitesse):
    result_str = ""
    for i in range(nb):
        result_str = result_str + ";[0:a:"+i+"]atempo="+vitesse
    result_str = result_str + " -map [v]"
    for i in range(nb):
        result_str = result_str + " -map 0:a:"+i
    return result_str

#Permet de générer les paramètres pour le volume
def genVolumeParam(nb_codec, volume):
    result_str = "-af volume="+volume
    for i in range(nb_codec):
        result_str = result_str + "-map 0:a:"+i+" "
    return result_str




"""

Démarrage du script

"""

#On vérfie si la table priority est vide ou non
empty = checkIfPrioEmpty()

if empty:
    table = "normal"
else:
    table = "priority"

#On initialise un dictionnaire qui contiendra les commandes à lancer
commands = {}




#Co à la BDD pour récupérer les tâches à effectuer en fonction de leur position dans la queue
with sqlite3.connect('/mnt/glusterfs/bdd/provisioning.db') as DBconn:
    c = DBconn.cursor()
    c.execute("SELECT command FROM "+ table +" WHERE order_queue = (SELECT min(order_queue) from "+ table +");")
    data = c.fetchall()
DBconn.close()


#Si la table n'est pas vide
if data:
    for i in range(len(data)):
        #on reconstruit les commandes stockées en BDD en dictionnaire
        commands = {**commands, **eval(data[i][0])} #merge les dictionnaires

    if isUnixPath(commands['input-video']['path']):
        fname = getUnixFilename(commands['input-video']['path'])
    else:
        fname = getWindowsFilename(commands['input-video']['path'])

    #Ici il faut mettre le chemin ou est téléchargé votre fichier uploadé via node-red
    #pour notre part il se situe sur glusterfs (système de fichiers distribués)
    filepath = "/mnt/glusterfs/"+fname
    useless, file_extension = os.path.splitext(filepath) #useless = le chemin vers le fichier sans son extension || file_extension = l'extension du fichier ...

    #On test si le fichier existe (s'il est arrivé sur le serveur)
    if os.path.isfile(filepath):
        ffprobeJson = ffprobeToJson(filepath)
        ffprobePython = jsonToPython(ffprobeJson)
        stream = streamsData(ffprobePython)

        #on créé un uuid pour qu'il n'y ait pas de problème de nommage des tâches
        short_uuid = str(uuid.uuid4())[:8]
        task_name = short_uuid+ "_split_" + fname
        #On créé le path du fichier à traiter dans le container ici car subprocess.call n'aime pas trop les %d
        path_to_file_in_container = "/data/"+short_uuid+"_"+fname+"%d"+file_extension
        #On lance le split
        subprocess.call(["docker","service","create","--mount","type=bind,src=/mnt/glusterfs,dst=/data","--mode=global","--restart-condition=none","--name="+task_name,"shellmaster/armhf-ffmpeg","-y","-i","/data/"+fname,"-f","segment","-reset_timestamps","1","-map","0",path_to_file_in_container])
        #fzefzef
        while not isCompleted(task_name):
            time.sleep(3)
        subprocess.call(["docker", "service", "rm", task_name])
        #on lance les commandes
        for i in commands:
            if i == "speed":
                print("commande speed : ffmpeg -i MONFICHIER -filter_complex [0:v]setpts=" + commands['speed']['video']+"*PTS[v]"+genSpeedParam(countAudioStream(stream), commands['speed']['sound'])) + "MONFICHIER")
            elif i == "custom":
                print("dcommande custom : ")
            elif i == "resolution":
                print("commande resolution : ")
            elif i == "volume":
                print("commande volume : ")
            elif i == "encoding":
                print("commande encoding : ")

    else:
        print("le ficher existe pas ou n'a pas encore été téléchargé sur le serveur")
        #on fait rien du coup ou on peut wait

else:
    print("les deux tables sont vides")
    #on boucle
