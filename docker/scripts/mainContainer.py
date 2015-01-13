#!/usr/bin/python3
# -*-coding:utf-8 -*

import os
import random
import subprocess
import numpy
import utils
import time
from chrome import Chrome
from firefox import Firefox

############### Container Class
class Container(object):

    ### Environment variables
    homeFolder = '/home/blink/'
    allPluginsFolder = homeFolder+'plugins/'
    allFontsFolder = homeFolder+'fonts/'
    allBrowsersFolder = homeFolder+'browsers/'

    profileFolder = homeFolder+'profile/'
    dataFile = profileFolder+'data.json'
    encryptedDataFile = dataFile+".gpg"

    destFontsFolder = '/home/blink/.fonts/'
    destPluginsFolder = '/home/blink/.mozilla/plugins/'

    averageNbFonts = 261.0094
    sdFonts = 91.45935
    averageNbPlugins = 12.6303
    sdPlugins = 5.7451

    ### Init
    def __init__(self):

        #List of plugins
        self.userP = []
        self.pluginsList = []
        self.userPlugins = []
        for root, dirs, files in os.walk(Container.allPluginsFolder):
            for file in files:
                self.pluginsList.append(os.path.abspath(os.path.join(root, file)))
                if file in self.userP :
                    self.userPlugins.append(os.path.abspath(os.path.join(root, file)))

        #List of fonts
        self.fontsList = []
        for root, dirs, files in os.walk(Container.allFontsFolder):
            for file in files:
                self.fontsList.append(os.path.abspath(os.path.join(root, file)))

    ### PLUGINS
    def selectPlugins(self):
        nbRandomPlugins = int(numpy.random.normal(loc=Container.averageNbPlugins,scale=Container.sdPlugins))
        while nbRandomPlugins < 1 :
            nbRandomPlugins = int(numpy.random.normal(loc=Container.averageNbPlugins,scale=Container.sdPlugins))

        randomPluginsList = [file for file in self.pluginsList if file not in self.userPlugins]
        finalPluginsList = list(self.userPlugins)
        if nbRandomPlugins > len(randomPluginsList):
            finalPluginsList = list(self.pluginsList)
        else :
            finalPluginsList.extend(random.sample(randomPluginsList,nbRandomPlugins))

        #We remove old mozilla files to be sure to correctly load plugins
        subprocess.call("find ~/.mozilla -name pluginreg.dat -type f -exec rm {} \;", shell=True)

        #We remove the old plugins and copy the new ones
        subprocess.call("rm -rf "+Container.destPluginsFolder+"*",shell=True)
        for plugin in finalPluginsList:
            subprocess.call(["cp",plugin,Container.destPluginsFolder])

    ### FONTS
    def selectFonts(self):
        nbRandomFonts = int(numpy.random.normal(loc=Container.averageNbFonts,scale=Container.sdFonts))
        while nbRandomFonts < 1:
            nbRandomFonts = int(numpy.random.normal(loc=Container.averageNbFonts,scale=Container.sdFonts))
        finalFontsList = random.sample(self.fontsList,nbRandomFonts)

        #We remove the old fonts, recreate the link to the user fonts and copy the new ones
        subprocess.call("rm -rf "+Container.destFontsFolder+"*",shell=True)
        for font in finalFontsList:
            subprocess.call(["cp",font,Container.destFontsFolder])

    ### BROWSERS
    @staticmethod
    def selectBrowser():
        browsersList = os.listdir(Container.allBrowsersFolder)
        browsersList.remove("extensions")
        return browsersList[random.randint(0,len(browsersList)-1)]

    ### Check existence of data file
    # If the file does not exist, it is created
    # If the file is encrypted, it will be unencrypted
    @staticmethod
    def checkDataFile():
        if os.path.isfile(Container.encryptedDataFile):
            #We decrypt it
            #TO IMPLEMENT
            t = 1
        elif not os.path.isfile(Container.dataFile):
            jsonData = {"bookmarks":
                            [{"name":"Bookmarks Toolbar","children":[],"type":"folder"},
                             {"name":"Bookmarks Menu","children":[],"type":"folder"},
                             {"name":"Unsorted Bookmarks","children":[],"type":"folder"}],
                        "openTabs":[],
                        "passwords":[],
                        "passwordStorage":"false",
                        "passwordEncryption":"false",
                        "browser":"Firefox"}
            utils.writeJSONDataFile(jsonData,Container.dataFile)


############### Main
def main():
    print("Blink Container Main script")

    #Change the working directory to the Shared folder
    os.chdir(Container.homeFolder)

    #We create an instance of Container
    blink = Container()

    #We check the Data file with the complete user profile
    blink.checkDataFile()

    #We chose the fonts and the plugins
    blink.selectFonts()
    blink.selectPlugins()

    if blink.selectBrowser() == 'chrome':
        browser = Chrome()
    else :
        browser = Firefox()
    #We import the user profile inside the browser
    browser.importData()

    #We initialise a boolean to indicate if the
    #VM must be shutdown
    shutdown = False

    while not shutdown :
        #We launch the browser
        browserProcess = browser.runBrowser()

        #We wait for either the browsing session to be finished
        while not isinstance(browserProcess.poll(),int):
            time.sleep(10)

        encryption = browser.exportData()

        #Encrypt file if the encryption is activated

        #We write a file to signal the host to shutdown all running VMs
        #subprocess.call("touch "+VM.sharedFolder+"VM.shutdown", shell=True)

        #We finish the execution of the script
        shutdown = True

        #else :
        #We terminate the browser process
        #browserProcess.kill()

        #We switch the list of plugins and fonts
        #machine.selectFonts()
        #machine.selectPlugins()
        #We remove the "browser.switch" file
        #subprocess.call("rm "+VM.sharedFolder+"browser.switch",shell=True)


if __name__ == "__main__":
    main()