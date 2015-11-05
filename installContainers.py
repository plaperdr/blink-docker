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
    buildDockerImageHub("blinkfedorig","os/fedora/")
    buildDockerImageHub("blinkubuorig","os/fedora/ubuntu")

    #Update Dockerfiles to include the right user/group ID
    #And build the final OS images
    updateGroupUserIDs()
    buildDockerImageNoPullLocal("blinkfed","run/fedora/")
    buildDockerImageNoPullLocal("blinkubu","run/ubuntu/")

    #Build plugins/fonts/browsers images
    #and instantiate containers
    buildDockerImageHub("blinkbrowsers","browsers/")
    instantiateContainer("blinkbrowsers")
    buildDockerImageHub("blinkfonts","fonts/")
    instantiateContainer("blinkfonts")

    print("Installation of Blink containers complete")

if __name__ == "__main__":
    main()