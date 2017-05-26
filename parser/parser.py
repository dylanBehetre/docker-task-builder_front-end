#!/usr/bin/env python
import pika
import sys
import json
from pprint import pprint

#check if the number of parameter is correct
if (len(sys.argv) != 2):
    sys.exit("Missing input parameter")


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

    if (not ip or not op):
        sys.exit("Missing input or output")

    list_tasks = {} #json final
    for i in range(1, len(data)):
        intermediateJSON = {}
        list_tasks[data[i]['type']] = []

        if data[i]['type'] == 'custom':
            intermediateJSON['image'] = data[i]['nomImage']
            intermediateJSON['command'] = data[i]['commandeRun']
            list_tasks[data[i]['type']].append(intermediateJSON)

        elif data[i]['type'] == 'encoding':
            intermediateJSON['codec'] = data[i]['encoding']
            list_tasks[data[i]['type']].append(intermediateJSON)

        elif data[i]['type'] == 'input-video':
            intermediateJSON['path'] = data[i]['video']
            list_tasks[data[i]['type']].append(intermediateJSON)

        elif data[i]['type'] == 'output-video':
            intermediateJSON['path'] = data[i]['video']
            list_tasks['priority'] = data[i]['priority']
            list_tasks[data[i]['type']].append(intermediateJSON)

        elif data[i]['type'] == 'resolution':
            if data[i]['resolution'] == "480p":
                intermediateJSON['width'] = '720'
                intermediateJSON['height'] = '480'
            elif data[i]['resolution'] == "720p":
                intermediateJSON['width'] = '1280'
                intermediateJSON['height'] = '720'
            elif data[i]['resolution'] == "1080p":
                intermediateJSON['width'] = '1920'
                intermediateJSON['height'] = '1080'
            list_tasks[data[i]['type']].append(intermediateJSON)


        elif data[i]['type'] == 'speed':
            intermediateJSON['video'] = data[i]['vitesseVideo']
            intermediateJSON['sound'] = data[i]['vitesseSon']
            list_tasks[data[i]['type']].append(intermediateJSON)


        elif data[i]['type'] == 'volume':
            intermediateJSON['value'] = data[i]['volume']
            list_tasks[data[i]['type']].append(intermediateJSON)

data_file.closed

out_file = open("parsed_"+sys.argv[1],'w')
json.dump(list_tasks, out_file)
out_file.closed

priority = list_tasks['priority']
pprint(list_tasks)



'''
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='test_provisioning', type=priority)
'''
'''
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
print(" [x] Sent %r" % message)
connection.close()
'''
