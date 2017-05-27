#!/usr/bin/python

import subprocess
import time

subprocess.call(["docker","service","create","--mount","type=bind,src=/home/toinou/Documents,dst=/files","--mode=global","--restart-condition=none","--name=test","sjourdan/ffmpeg","-y","-i","/files/video.mp4","-acodec","copy","-f","segment","-vcodec","libx264","-reset_timestamps","1","-map","0","/files/output%d.mp4"])
toto = False
while not toto:
    result = subprocess.getstatusoutput("docker service ps test | sed -n 2p | sed -E \"s/[[:space:]]+/ /g\" | cut -f6 -d' '")[1]
    print(result)
    if result == "Complete":
        print("Processus complété")
    time.sleep(5)
