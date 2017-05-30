#!/usr/bin/python
import sys
import json
import sqlite3
import uuid


#functions definitions
#check queue position in priority table
def checkPriorityQueue():
    with sqlite3.connect('bdd/provisioning.db') as DBconn:
        c = DBconn.cursor()
        c.execute("SELECT MAX(order_queue) FROM priority;")
        position = c.fetchone()[0]
    DBconn.close()
    if position is None:
        position = 1
    else:
        position = int(position) + 1
    return position

#check queue position in non-priority table
def checkNormalPosition():
    with sqlite3.connect('bdd/provisioning.db') as DBconn:
        c = DBconn.cursor()
        c.execute("SELECT MAX(order_queue) FROM normal;")
        position = c.fetchone()[0]
    DBconn.close()
    if position is None:
        position = 1
    else:
        position = int(position) + 1
    return position

#check if tasks are priority or not
def checkIfPrio(json_data):
    for i in range(1, len(data)):
        if json_data[i]['type'] == 'output-video':
            if json_data[i]['priority'] == "0":
                return False
            return True

def insertIntoTable(booleanPrio, json, order_task, order_queue, uuid):
    with sqlite3.connect('bdd/provisioning.db') as DBconn:
        c = DBconn.cursor()
        if booleanPrio:#insert dans table priority
            print("INSERT INTO priority VALUES (\""+uuid+"\", json, \""+ str(i) +"\", \""+ str(position) +"\")")
            c.execute("INSERT INTO priority VALUES (?, ?, ?, ?);", (uuid, str(json), str(i), str(position)))
        else:
            print("INSERT INTO normal VALUES (\""+uuid+"\", json, \""+ str(i) +"\", \""+ str(position) +"\")")
            c.execute("INSERT INTO normal VALUES (?, ?, ?, ?);", (uuid, str(json), str(i), str(position)))
        DBconn.commit()
        #fermer la table


#check if the number of parameter is correct
if (len(sys.argv) != 2):
    sys.exit("Missing input parameter")

#load the JSON file
with open(sys.argv[1], 'r') as data_file:
    data = json.load(data_file)

#check if input and output are here
op = False
ip = False
for i in range(1, len(data)):
    if data[i]['type'] == "output-video":
        op = True
    elif data[i]['type'] == "input-video":
        ip = True

#if input or output is missing : invalid JSON
if (not ip or not op):
    sys.exit("Missing input or output : invalid JSON")


priority = checkIfPrio(data)
if priority:
    position = checkPriorityQueue()
else:
    position = checkNormalPosition()

list_tasks = {} #json final
uuid = str(uuid.uuid4())[:8]
for i in range(1, len(data)):
    intermediateJSON = {}
    finalJSON = {}
    list_tasks[data[i]['type']] = []

    if data[i]['type'] == 'custom':
        intermediateJSON['image'] = data[i]['nomImage']
        intermediateJSON['command'] = data[i]['commandeRun']
        finalJSON['custom'] = intermediateJSON
        insertIntoTable(priority, finalJSON, i, position, uuid)

    elif data[i]['type'] == 'encoding':
        intermediateJSON['codec'] = data[i]['encoding']
        finalJSON['encoding'] = intermediateJSON
        insertIntoTable(priority, finalJSON, i, position, uuid)

    elif data[i]['type'] == 'input-video':
        intermediateJSON['path'] = data[i]['video']
        finalJSON['input-video'] = intermediateJSON
        insertIntoTable(priority, finalJSON, i, position, uuid)

    elif data[i]['type'] == 'output-video':
        intermediateJSON['path'] = data[i]['videoName']
        finalJSON['output-video'] = intermediateJSON
        insertIntoTable(priority, finalJSON, i, position, uuid)

    elif data[i]['type'] == 'resolution':
        if data[i]['resolution'] == "480p":
            intermediateJSON['width'] = '720'
            intermediateJSON['height'] = '480'
            finalJSON['resolution'] = intermediateJSON
            insertIntoTable(priority, finalJSON, i, position, uuid)

        elif data[i]['resolution'] == "720p":
            intermediateJSON['width'] = '1280'
            intermediateJSON['height'] = '720'
            finalJSON['resolution'] = intermediateJSON
            insertIntoTable(priority, finalJSON, i, position, uuid)

        elif data[i]['resolution'] == "1080p":
            intermediateJSON['width'] = '1920'
            intermediateJSON['height'] = '1080'
            finalJSON['resolution'] = intermediateJSON
            insertIntoTable(priority, finalJSON, i, position, uuid)


    elif data[i]['type'] == 'speed':
        intermediateJSON['video'] = data[i]['vitesseVideo']
        intermediateJSON['sound'] = data[i]['vitesseSon']
        finalJSON['speed'] = intermediateJSON
        insertIntoTable(priority, finalJSON, i, position, uuid)

    elif data[i]['type'] == 'volume':
        intermediateJSON['value'] = data[i]['volume']
        finalJSON['volume'] = intermediateJSON
        insertIntoTable(priority, finalJSON, i, position, uuid)

data_file.close()
