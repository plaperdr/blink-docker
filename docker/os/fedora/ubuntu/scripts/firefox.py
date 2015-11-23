#!/usr/bin/python3
# -*-coding:utf-8 -*

import subprocess
from browser import Browser,utils

class FirefoxBase(Browser):
    
    def __init__(self,path):
        super().__init__()
        self.firefoxPath = path
        
    def importData(self):
        pass
            
    def exportData(self):
        jsonExportData = utils.readJSONDataFile(self.dataPath)
        return jsonExportData["passwordEncryption"]
            
    def runBrowser(self):
        return subprocess.Popen("LD_PRELOAD=/home/blink/ldpreload/modUname.so "+self.firefoxPath+" -no-remote -setDefaultBrowser -profile /home/blink/.mozilla/firefox/blink.default", shell=True)

class FirefoxRepo(FirefoxBase):
    def __init__(self):
        super().__init__("firefox")

class Firefox(FirefoxBase):
    def __init__(self):
        super().__init__("./browsers/firefox-latest/firefox")

class FirefoxESR(FirefoxBase):
    def __init__(self):
        super().__init__("./browsers/firefox-latest-esr/firefox")

