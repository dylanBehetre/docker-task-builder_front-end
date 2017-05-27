#!/usr/bin/python

import sqlite3
import json
import subprocess

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

empty = checkIfPrioEmpty()

if empty:
    table = "normal"
else:
    table = "priority"

commands = {}
with sqlite3.connect('bdd/provisioning.db') as DBconn:
    c = DBconn.cursor()
    c.execute("SELECT command FROM "+ table +" WHERE order_queue = (SELECT min(order_queue) from "+table +");")
    data = c.fetchall()
DBconn.close()
if data:
    print("une des tables n'est pas vide")
    for i in range(len(data)):
        commands = {**commands, **eval(data[i][0])} #merge les dictionnaires
    #on a récup les commandes à lancer
    #on lance d'abord le split
    subprocess.call(["docker","service","create","--mount","type=bind,src=/home/toinou/Documents,dst=/files","--mode=global","--restart-condition=none","--name=test","sjourdan/ffmpeg","-y","-i","/files/video.mp4","-acodec","copy","-f","segment","-vcodec","libx264","-reset_timestamps","1","-map","0","/files/output/d.mp4"])

else:
    print("les deux tables sont vides")





##simulation lancer service faire un bon nommage
##simulation savoir si script terminé dans docker service ps puis merge dans script différent
