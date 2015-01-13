#!/usr/bin/python3
# -*-coding:utf-8 -*

import re
import os
import sys
import random
import subprocess

osImages = ["blinkfed","blinkubu"]

def checkInstallation():
    #Check the presence of the three main containers
    #and the two main OS images
    regExp = re.compile("Exited \(0\).*?blink(fonts|browsers|plugins).*?\\n")
    output = subprocess.check_output(["sudo","docker","ps","-a"]).decode()
    if len(regExp.findall(output)) != 3:
        sys.exit("Blink is not installed")

    output = subprocess.check_output(["sudo","docker","images"]).decode()
    for image in osImages :
        if image not in output:
            sys.exit("Blink is not installed")



def main():

    if not os.path.isfile("installComplete"):
        checkInstallation()
        print("Installation verified")
        subprocess.call(["touch","installComplete"])

    print("Launching Blink browsing environment")
    downloadsPath =  os.path.abspath("data/downloads")
    profilePath = os.path.abspath("data/profile")
    launchCommand = "sudo docker run -ti --rm -e DISPLAY " \
                    "-v /tmp/.X11-unix:/tmp/.X11-unix " \
                    "-v "+downloadsPath+":/home/blink/Downloads " \
                    "-v "+profilePath+":/home/blink/profile " \
                    "--volumes-from blinkbrowsers " \
                    "--volumes-from blinkplugins " \
                    "--volumes-from blinkfonts "
    chosenImage = osImages[random.randint(0,len(osImages)-1)]
    print("Image "+chosenImage+" chosen")
    subprocess.call(launchCommand+chosenImage,shell=True)

    print("End of script")

if __name__ == "__main__":
    main()
