#!/usr/bin/python

import sqlite3
import json

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

commands = []
with sqlite3.connect('bdd/provisioning.db') as DBconn:
    c = DBconn.cursor()
    c.execute("SELECT command FROM "+ table +" WHERE order_queue = (SELECT min(order_queue) from "+table +");")
    data = c.fetchall()
    for i in range(0, len(data)):
        commands.append(data[i][0])
DBconn.close()
print(commands)
print("from "+table)
