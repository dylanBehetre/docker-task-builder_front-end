#!/usr/bin/python
import os
import re

strUnix = "/home/toto/documents/monfichier.fdp"
strWindows = "C:\mdr\le_chemin\de_merde\caca.fdp"

def getUnixFilename(path):
    result = path
    result = result[::-1] #on met retourne la string à l'envers
    result = result.split("/") #on split pour enlever les /
    result = result[0][::-1] #on remet le nom du fichier à l'endroit
    return result


def getWindowsFilename(path):
    result = path
    result = result[::-1] #on met retourne la string à l'envers
    result = result.split("\\") #on split pour enlever les \
    result = result[0][::-1] #on remet le nom du fichier à l'endroit
    return result


strUnix = getUnixFilename(strUnix)
strWindows = getWindowsFilename(strWindows)
print(strWindows)
print(strUnix)
