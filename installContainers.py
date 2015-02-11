#!/usr/bin/python3
# -*-coding:utf-8 -*

import os
import sys
import shutil
import zipfile
import subprocess
import urllib.request
from urllib.error import URLError

def downloadFile(file):
    try:
        print("Downloading "+file+"...")
        urllib.request.urlretrieve("http://amiunique.irisa.fr/"+file, file)
    except URLError:
        sys.exit("Error downloading "+file)
    print("Download of "+file+" complete")


def extractFile(file,path):
    try:
        downloadedZip = zipfile.ZipFile(file)
        print("Extracting "+file+" in "+path+"...")
        zipfile.ZipFile.extractall(downloadedZip,path)
    except zipfile.BadZipFile:
        sys.exit("Bad zip file detected")
    print("Extraction of "+file+" complete")
    os.remove(file)

def pullDockerImage(name):
    print("Pulling "+name+" image from the Docker registry")
    subprocess.call(["sudo","docker","pull",name])

def buildDockerImage(name,path):
    print("Building Docker image "+name+" with "+path)
    subprocess.call(["sudo","docker","build","-t",name,path])

def instantiateContainer(name):
    print("Running container "+name)
    subprocess.call(["sudo","docker","run","--name",name,name])

def main():
    print("Blink Installation script")

    #Change current working directory
    os.chdir("docker")

    #Check to see if Docker is installed
    if "command not found" in subprocess.check_output(["sudo","docker","info"]).decode():
        sys.exit("Docker not installed. Install Docker to process with the installation.")

    #Download plugins and fonts if not present
    if not os.path.isdir("fonts/ALL_FONTS"):
        downloadFile("fonts.zip")
        extractFile("fonts.zip","fonts")
    if not os.path.isdir("plugins/ALL_PLUGINS"):
        downloadFile("plugins.zip")
        extractFile("plugins.zip","plugins")

    #Download latest Docker images
    pullDockerImage("fedora")
    pullDockerImage("ubuntu")

    #Build OS images
    shutil.copyfile("os/fedora/Dockerfile","scripts/Dockerfile")
    buildDockerImage("blinkfed","scripts/")
    shutil.copyfile("os/ubuntu/Dockerfile","scripts/Dockerfile")
    buildDockerImage("blinkubu","scripts/")

    #Build plugins/fonts/browsers images
    #and instantiate containers
    buildDockerImage("blinkbrowsers","browsers/")
    instantiateContainer("blinkbrowsers")
    buildDockerImage("blinkfonts","fonts/")
    instantiateContainer("blinkfonts")
    buildDockerImage("blinkplugins","plugins/")
    instantiateContainer("blinkplugins")

    print("Installation of Blink containers complete")

if __name__ == "__main__":
    main()