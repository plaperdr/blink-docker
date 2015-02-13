#!/usr/bin/python3
# -*-coding:utf-8 -*

import os
import json
import pickle
import subprocess
from pprint import pprint
from subprocess import CalledProcessError
from browser import Browser,utils

class Chrome(Browser):
    
    def __init__(self):
        super().__init__()
        self.bookmarksFile = "Bookmarks"
        self.openTabsFile = "shared.pkl"
        self.passwordsFile = "Login\ Data"
        self.profileFolder = utils.relativeToAbsoluteHomePath("~/.config/google-chrome/Default/")
        
        jsonDataStructure = {"bookmarks":[{"name":"Bookmarks Toolbar",
                                    "children":[],
                                    "type":"folder"},
                                   {"name":"Bookmarks Menu",
                                    "children":[],
                                    "type":"folder"},
                                   {"name":"Unsorted Bookmarks",
                                    "children":[],
                                    "type":"folder"}
                                   ],
                      "openTabs":[],
                      "passwords":[],
                      "passwordStorage":False,
                      "passwordEncryption":False,
                      "browser":"Chrome"}
        
        if os.path.isfile(self.dataPath):
            self.jsonImportData = utils.readJSONDataFile(self.dataPath)
            self.passwordStorage = self.jsonImportData["passwordStorage"]
            self.passwordEncryption = self.jsonImportData["passwordEncryption"]
            
        else :
            self.jsonImportData = jsonDataStructure
            self.passwordStorage = False
            self.passwordEncryption = False
        
        self.jsonExportData  = jsonDataStructure
        self.jsonExportData["passwordStorage"] = self.passwordStorage 
        self.jsonExportData["passwordEncryption"] = self.passwordEncryption
    
    #################################  BROWSER  #################################
    @staticmethod
    def find(name, path):
        for root, dirs, files in os.walk(path):
            if name in files:
                return os.path.join(root, name)
            
    def runBrowser(self):
        chromePath = self.find("chrome","./browsers/chrome/")
        return subprocess.Popen(chromePath+" --password-store=basic --no-sandbox --load-extension=/home/blink/browsers/extensions/ups/ --no-default-browser-check --no-first-run",shell=True)
    
        
    #################################  BOOKMARKS  #################################
    def importBookmarks(self):
        chromeJsonData = { "roots": {"bookmark_bar":{"children":{},
                                                     "name":"Bookmarks Bar",
                                                     "type":"folder"},
                                     "other":{"children": {},
                                              "name" : "Other Bookmarks",
                                              "type":"folder"},
                                     "synced":{"children":{},
                                               "name":"Mobile Bookmarks",
                                               "type":"folder"}
                                     }, 
                          "version": 1,
                          "checksum": ""}
        chromeJsonData["roots"]["bookmark_bar"]["children"] = self.jsonImportData["bookmarks"][0]["children"]
        chromeJsonData["roots"]["other"]["children"] = self.jsonImportData["bookmarks"][1]["children"]
        chromeJsonData["roots"]["other"]["children"].extend(self.jsonImportData["bookmarks"][2]["children"])
        with open(self.profileFolder+self.bookmarksFile, 'w') as chromeBookmarks:
            json.dump(chromeJsonData, chromeBookmarks)
        
        
    def exportBookmarks(self):
        if os.path.isfile(self.profileFolder+self.bookmarksFile):
            with open(self.profileFolder+self.bookmarksFile, 'r') as chromeBookmarks:
                chromeJsonData = json.load(chromeBookmarks)
            self.jsonExportData["bookmarks"][0]["children"] = chromeJsonData["roots"]["bookmark_bar"]["children"]
            self.jsonExportData["bookmarks"][1]["children"] = chromeJsonData["roots"]["other"]["children"]
    
    #################################  OPEN TABS  #################################
    def importOpenTabs(self):
        chromeTabs = json.dumps({"openTabs": self.jsonImportData["openTabs"],"passwordEncryption": self.jsonImportData["passwordEncryption"],"passwordStorage": self.jsonImportData["passwordStorage"]})
        with open(self.profileFolder+self.openTabsFile,'wb') as sharedFile:
            pickle.dump(chromeTabs,sharedFile,protocol=2)
    
    
    def exportOpenTabs(self):
        if os.path.isfile(self.profileFolder+self.openTabsFile):
            with open(self.profileFolder+self.openTabsFile,'rb') as sharedFile:
                jsonTabs = pickle.load(sharedFile)
            data = json.loads(jsonTabs)
            self.passwordStorage = data["passwordStorage"]
            self.jsonExportData["passwordStorage"] = self.passwordStorage
            self.passwordEncryption = data["passwordEncryption"]
            self.jsonExportData["passwordEncryption"] = self.passwordEncryption
            for tab in data["openTabs"]:
                url = tab["url"]
                self.jsonExportData["openTabs"].append({"url":url})
        
            
    #################################  PASSWORDS  #################################
    def importPasswords(self):
        subprocess.call("cp -f /home/blink/browsers/extensions/Login\ Data ~/.config/google-chrome/Default/Login\ Data",shell=True)
        if self.jsonImportData["passwords"] != []:
            passwordsList = json.loads(json.dumps(self.jsonImportData["passwords"]))
                
            for passwordData in passwordsList:
                commandStart = "echo \"INSERT INTO Logins(origin_url,action_url,username_value,password_value,signon_realm,ssl_valid,preferred,date_created,blacklisted_by_user,scheme) VALUES('"
                commandValues = passwordData["hostname"]+"','"+passwordData["formSubmitURL"]+"','"+passwordData["username"]+"','"+passwordData["password"]+"','"+passwordData["hostname"]+"',"
                if "https" in passwordData["hostname"]:
                    commandValues += "1"
                else :
                    commandValues += "0"
                commandEnd = ",0,0,0,0);\" | sqlite3 ~/.config/google-chrome/Default/Login\ Data | grep -v '^|$'"
                subprocess.call(commandStart+commandValues+commandEnd,shell=True)
            del passwordsList
        
    
    def exportPasswords(self):
        selectCommand = "echo 'SELECT origin_url,username_value, password_value,action_url FROM logins;' | sqlite3 ~/.config/google-chrome/Default/Login\ Data | grep -v '^|$'"
        try :
            passwordsData = subprocess.check_output(selectCommand,shell=True)
            passwordsData = passwordsData.decode()
            passwordsList = []
            for line in passwordsData.splitlines():
                data = line.split('|')
                passwordsList.append({"hostname":data[0],
                                        "username":data[1],
                                        "password":data[2],
                                        "formSubmitURL":data[3],
                                         })
            
            self.jsonExportData["passwords"] = passwordsList
            
        except CalledProcessError:
            self.jsonExportData["passwords"] = ""
        
    #################################  DATA  #################################
    def importData(self):
        if os.path.isdir("/home/blink/.config/google-chrome/Default/"):
            print("Data import")
            self.importBookmarks()
            self.importOpenTabs()
            self.importPasswords()
        
        
    def exportData(self):
        print("Data export")
        self.exportBookmarks()
        self.exportOpenTabs()
        self.exportPasswords()
        utils.writeJSONDataFile(self.jsonExportData, self.dataPath)
        return self.jsonExportData["passwordEncryption"]

