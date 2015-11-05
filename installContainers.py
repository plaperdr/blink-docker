#!/usr/bin/python3
# -*-coding:utf-8 -*

from installUtils import *

def main():
    print("Blink Installation script")

    #Change current working directory
    os.chdir("docker")

    #Check to see if Docker is installed
    if "command not found" in subprocess.check_output(["sudo","docker","info"]).decode():
        sys.exit("Docker not installed. Install Docker to process with the installation.")

    #Build OS images
    buildDockerImage("blinkfedorig","os/fedora/",True)
    buildDockerImage("blinkubuorig","os/fedora/ubuntu",True)

    #Update Dockerfiles to include the right user/group ID
    #And build the final OS images
    updateGroupUserIDs()
    buildDockerImageNoPull("blinkfed","run/fedora/")
    buildDockerImageNoPull("blinkubu","run/ubuntu/")

    #Build plugins/fonts/browsers images
    #and instantiate containers
    buildDockerImage("blinkbrowsers","browsers/",True)
    instantiateContainer("blinkbrowsers")
    buildDockerImage("blinkfonts","fonts/",True)
    instantiateContainer("blinkfonts")

    print("Installation of Blink containers complete")

if __name__ == "__main__":
    main()