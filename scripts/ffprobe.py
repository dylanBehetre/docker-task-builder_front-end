'''
Launches ffprobe on a file and returns 2 arguments
1st argument : a list of the streams present in the media
2nd argument : the number of streams
'''

import subprocess
import json

def ffprobeToJson( theFile ):
    json = subprocess.check_output(
        'ffprobe -v quiet -print_format json -show_format -show_streams %s ' %theFile,
        stderr=subprocess.STDOUT,
        shell=True)
    return json

def streamsData( pythonJson ):
    streams = pythonJson['streams']
    length = len(streams) # Number of streams present in the mdeia
    return streams,length


def jsonToPython( theJson ):
    return json.loads(theJson)

def mainFunction():
    ffprobeJson = ffprobeToJson("../input/Scarecrow.mp4")
    ffprobePython = jsonToPython(ffprobeJson)
    return streamsData(ffprobePython)
