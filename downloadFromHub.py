#!/usr/bin/python3
# -*-coding:utf-8 -*

from installUtils import *
import uuid
import json

def setupTorProxy():
    #Pull the Tor proxy image
    subprocess.call(["sudo","docker","pull","jess/tor-proxy"])

    #Instantiate the container
    subprocess.call(["sudo","docker","run","-d","--restart","always","-p","9050:9050","--name","torproxy","jess/tor-proxy"])

    #Stop the container
    subprocess.call(["sudo","docker","stop","torproxy"])

def main():
    print("Blink Download script")

    #Change current working directory
    os.chdir("docker")

    #Check to see if Docker is installed
    if "command not found" in subprocess.check_output(["sudo","docker","info"]).decode():
        sys.exit("Docker not installed. Install Docker to process with the installation.")

    #Pull all Docker images
    for image in dockerImages:
        pullDockerImage(image)

    #Update Dockerfiles to include the right user/group ID
    #And build the final OS images
    updateGroupUserIDs()
    buildDockerImageLocal("blinkfed","run/fedora/")
    buildDockerImageLocal("blinkubu","run/ubuntu/")

    #Instantiate containers
    instantiateContainer("blinkbrowsers")
    instantiateContainer("blinkfonts")

    #Setup the Tor proxy container
    setupTorProxy()

    #Generation of exp ID
    expID = str(uuid.uuid4())

    #Write the ID to a blank data profile
    emptyJson = {"bookmarks":[{"name":"Bookmarks Toolbar",
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
                      "browser":"Chrome",
                      "expID": expID}
    with open("data/profile/data.json","w") as f:
        json.dump(emptyJson,f)

    print("Please visit with your normal browser the following URL")
    print("http://amiunique.irisa.fr/fp#"+expID)

    print("Installation of Blink containers complete")

if __name__ == "__main__":
    main()