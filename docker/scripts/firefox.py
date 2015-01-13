#!/usr/bin/python3
# -*-coding:utf-8 -*

import time
import subprocess
from browser import Browser,utils

class Firefox(Browser):        
    
    def __init__(self):
        super().__init__()
        
    def importData(self):
        pass
            
    def exportData(self):
        jsonExportData = utils.readJSONDataFile(self.dataPath)
        return jsonExportData["passwordEncryption"]
            
    def runBrowser(self):
        return subprocess.Popen(["./browsers/firefox/firefox","-no-remote"])
