import ffprobe
import subprocess
import sys
import os
from subprocess import Popen, PIPE

def getFfprobe():
    streams,length = ffprobe.mainFunction( the_file )
    return streams, length

def countAudio( streams, length ):
    cpt = 0
    for s in streams:
        if(s['codec_type'] == 'audio'):
            list_audio.append(cpt)
            cpt++

def launchCommand():
    audioNumber = len(list_audio)
    command = ''
    baseName = os.path.basename(the_file)

    for audio in list_audio:
        cpt = 0
        command+='[%s:a]' %cpt

    print(command)
    print (subprocess.check_output(
        'ffmpeg -i %s -af volume=%s volume_%s' %(the_file, new_volume, baseName),shell=True))

def main():
    streams, length = getFfprobe()
    countAudio(streams, length)
    launchCommand()
    return

global list_audio
global the_file
global new_volume

list_audio = []
the_file = sys.argv[1]
new_volume = sys.argv[2]

main()
