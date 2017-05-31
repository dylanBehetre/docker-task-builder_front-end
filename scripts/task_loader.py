#!/usr/bin/python

import sqlite3
import json
import subprocess
import os.path
import time
import re


# select * from priority where order_queue = (select min(order_queue) from priority);

def checkIfPrioEmpty():
    with sqlite3.connect('bdd/provisioning.db') as DBconn:
        c = DBconn.cursor()
        c.execute("SELECT MAX(order_queue) FROM priority;")
        position = c.fetchone()[0]
    DBconn.close()
    if position is None:
        return True
    else:
        return False


def ffprobeToJson(theFile):
    json = subprocess.check_output(
        'ffprobe -v quiet -print_format json -show_format -show_streams %s ' %theFile,
        stderr=subprocess.STDOUT,
        shell=True)
    return json


def streamsData(pythonJson):
    streams = pythonJson['streams']
    length = len(streams) # Number of streams present in the mdeia
    return streams


def jsonToPython(theJson):
    return json.loads(theJson)


def isCompleted(task):
    result = subprocess.getstatusoutput("docker service ps "+task+" | sed -n 2p | sed -E \"s/[[:space:]]+/ /g\" | cut -f6 -d' '")[1]
    if result == "Complete":
        return True
    return False

def isUnixPath(path):
    pattern = re.compile("^\/$|(^(?=\/)|^\.|^\.\.)(\/(?=[^/\0])[^/\0]+)*\/?$")
    result = pattern.match(path)
    if result:
        return True
    return False

def getUnixFilename(path):
    result = path
    result = result[::-1] #on met retourne la string à l'envers
    result = result.split("\/") #on split pour enlever les /
    result = result[0][::-1] #on remet le nom du fichier à l'endroit
    return result


def getWindowsFilename(path):
    result = path
    result = result[::-1] #on met retourne la string à l'envers
    result = result.split("\\") #on split pour enlever les \
    result = result[0][::-1] #on remet le nom du fichier à l'endroit
    return result

def countAudioStream(stream):
    cpt = 0
    for i in stream:
        if (i['codec_type'] == "audio"):
            cpt = cpt + 1
    return cpt

def genSpeedParam(nb_codec, vitesse):
    result_str = ""
    for i in range(nb):
        result_str = result_str + ";[0:a:"+i+"]atempo="+vitesse
    result_str = result_str + " -map [v]"
    for i in range(nb):
        result_str = result_str + " -map 0:a:"+i
    return result_str

def genVolumeParam(nb_codec, volume):
    result_str = "-af volume="+volume
    for i in range(nb_codec):
        result_str = result_str + "-map 0:a:"+i+" "
    return result_str

empty = checkIfPrioEmpty()

if empty:
    table = "normal"
else:
    table = "priority"

commands = {}
with sqlite3.connect('bdd/provisioning.db') as DBconn:
    c = DBconn.cursor()
    c.execute("SELECT command FROM "+ table +" WHERE order_queue = (SELECT min(order_queue) from "+ table +");")
    data = c.fetchall()
DBconn.close()
if data:
    for i in range(len(data)):
        #on reconstruit les commandes stockées en BDD en dictionnaire
        commands = {**commands, **eval(data[i][0])} #merge les dictionnaires

    if isUnixPath(commands['input-video']['path']):
        fname = getUnixFilename(commands['input-video']['path'])
    else:
        fname = getWindowsFilename(commands['input-video']['path'])
    filepath = "/mnt/glusterfs/"+fname
    useless, file_extension = os.path.splitext(filepath) #useless = le chemin vers le fichier sans son extension || file_extension = l'extension du fichier ...
    if os.path.isfile(filepath):
        ffprobeJson = ffprobeToJson(filepath)
        ffprobePython = jsonToPython(ffprobeJson)
        stream = streamsData(ffprobePython)
        print("le fichier existe on va le split")
        short_uuid = str(uuid.uuid4())[:8]
        task_name = short_uuid+ "_split_" + fname
        subprocess.call(["docker","service","create","--mount","type=bind,src=/mnt/glusterfs,dst=/data","--mode=global","--restart-condition=none","--name="+task_name,"shellmaster/armhf-ffmpeg","-y","-i","/data/"+fname,"-f","segment","-reset_timestamps","1","-map","0","/data/"+short_uuid+"_"+fname+"%d."+file_extension])
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




##simulation lancer service faire un bon nommage
##simulation savoir si script terminé dans docker service ps puis merge dans script différent
