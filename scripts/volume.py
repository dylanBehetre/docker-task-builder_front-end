import ffprobe
import subprocess
import sys
from subprocess import Popen, PIPE

def getFfprobe():
    streams,length = ffprobe.mainFunction( the_file )
    return streams, length

def countAudio( streams, length ):
    for s in streams:
        if(s['codec_type'] == 'audio'):
            list_audio.append(s['index'])

def launchCommand():
    audioNumber = len(list_audio)
    print (subprocess.check_output(
        'ffmpeg -i %s -af volume=%s volume_%s' %(the_file, new_volume, the_file),shell=True))

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
