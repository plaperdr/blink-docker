import os
import sys
import zipfile
import subprocess
import urllib.request
from urllib.error import URLError

prefixRepoHub = "docker.io/plaperdr/"
prefixRepoLocal = "blink/"

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
    print("Pulling Docker image "+name)
    subprocess.call(["sudo","docker","pull",prefixRepoHub+name])

def buildDockerImageHub(name,path):
    print("Building Docker image "+name+" with "+path)
    subprocess.call(["sudo","docker","build","--pull","-t",prefixRepoHub+name,path])

def buildDockerImageLocal(name,path):
    subprocess.call(["sudo","docker","build","--pull","-t",prefixRepoLocal+name,path])

def buildDockerImageNoPullLocal(name,path):
    print("Building Docker image "+name+" with "+path)
    subprocess.call(["sudo","docker","build","-t",prefixRepoLocal+name,path])

def instantiateContainer(name):
    print("Running container "+name)
    subprocess.call(["sudo","docker","run","--name",name,prefixRepoHub+name])

def updateGroupUserIDs():
    #Get user ID
    userID = subprocess.check_output(["id","-u"]).decode().strip()

    #Get group ID
    groupID = subprocess.check_output(["id","-g"]).decode().strip()

    updateDockerfile("run/fedora/Dockerfile",userID,groupID)
    updateDockerfile("run/ubuntu/Dockerfile",userID,groupID)
    print("Dockerfile user/group IDs updated")

def updateDockerfile(filePath,userID,groupID):
    #Rewrite the Dockerfile with the correct user/group ID
    with open(filePath,'r') as f:
        newlines = []
        for line in f.readlines():
            if "uid" in line and "gid" in line:
                line = line.replace('uid=1000', 'uid='+userID)
                line = line.replace('gid=1000', 'gid='+groupID)
                newlines.append(line)
            else:
                newlines.append(line)
    with open(filePath, 'w') as f:
        for line in newlines:
            f.write(line)