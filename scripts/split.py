'''
BLABLA CA SPLIT FAUT DEFINIR LES NOMS
'''

import ffprobe
import sys
import subprocess

def getFfprobe():
    streams,length = ffprobe.mainFunction( file_fullpath )
    return streams, length

def launchCommand():
    print(subprocess.check_output(
        'ffmpeg -i %s -f segment -reset_timestamps 1 -map 0 OUTPUT%d.mp4' %file_fullpath,
        shell=True))

def main():
    streams, length = getFfprobe()
    launchCommand()

global file_fullpath

file_fullpath = sys.argv[1]

main()
