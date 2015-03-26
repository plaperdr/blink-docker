#!/usr/bin/python3
# -*-coding:utf-8 -*

from installUtils import *

dockerImages = ["blinkfedorig","blinkubuorig","blinkfonts","blinkbrowsers"]

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
    buildDockerImage("blinkfed","run/fedora/")
    buildDockerImage("blinkubu","run/ubuntu/")

    print("Installation of Blink containers complete")

if __name__ == "__main__":
    main()