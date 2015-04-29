#!/usr/bin/python3
# -*-coding:utf-8 -*

import json
from os.path import expanduser

def relativeToAbsoluteHomePath(path):
    """ Tranforms a relative home path into an absolute one
    Argument:
    path -- the path that may need transformation"""
    if "~" in path:
        return path.replace("~",expanduser("~"))
    else:
        return path

def readJSONDataFile(dataPath):
    with open(dataPath, 'r', encoding='utf-8') as dataFile:
        jsonImportData = json.load(dataFile)
    return jsonImportData

def writeJSONDataFile(jsonExportData, dataPath):
    with open(dataPath, 'w') as dataFile:
        json.dump(jsonExportData, dataFile,ensure_ascii=True)