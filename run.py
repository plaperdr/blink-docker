#!/usr/bin/python3
# -*-coding:utf-8 -*

import re
import os
import sys
import random
import datetime
import subprocess
import urllib.request
from installContainers import buildDockerImage,instantiateContainer

osImages = ["blinkfed","blinkubu"]
ubuntuName = "trusty"
fedoraName = "fc21"

downloadsPath =  os.path.abspath("data/downloads")
profilePath = os.path.abspath("data/profile")
ldpreloadPath = os.path.abspath("ldpreload")

def checkInstallation():
    #Check the presence of the two main containers
    #and the two main OS images
    regExp = re.compile("Exited \(0\).*?blink(fonts|browsers).*?\\n")
    output = subprocess.check_output(["sudo","docker","ps","-a"]).decode()
    if len(regExp.findall(output)) != 2:
        sys.exit("Blink is not installed")

    output = subprocess.check_output(["sudo","docker","images"]).decode()
    for image in osImages :
        if image not in output:
            sys.exit("Blink is not installed")

    #If the installation is correct, we generate the LD Preload libraries
    generateLibrairies()


def generateLibrairies():

    #Fedora
    #We retrieve the kernel version of Fedora
    #ex: 3.18.5-201.fc21.x86_64
    fedSource = urllib.request.urlopen("https://admin.fedoraproject.org/updates/kernel").read()
    fedKernel = re.search("kernel-(.{1,20}"+fedoraName+")((?!testing).)*?stable",str(fedSource)).group(1)+".x86_64"
    #We write the header file
    with open('ldpreload/modUname.h', 'w') as f:
            f.write("#define RELEASE \""+fedKernel+"\"")
    #We compile the library
    subprocess.call(["gcc","-Wall","-fPIC","-shared","-o","ldpreload/modFedUname.so","ldpreload/modUname.c"])

    #Ubuntu
    #We retrieve the kernel version of Ubuntu
    #ex: 3.13.0-24-generic
    ubuSource = urllib.request.urlopen("http://packages.ubuntu.com/search?keywords=linux-image&searchon=names&suite="+
                                       ubuntuName+"&section=main").read()
    ubuKernel = re.search("linux-image-(.*?)\">",str(ubuSource)).group(1)
    #We write the header file
    with open('ldpreload/modUname.h', 'w') as f:
            f.write("#define RELEASE \""+ubuKernel+"\"")
    #We compile the library
    subprocess.call(["gcc","-Wall","-fPIC","-shared","-o","ldpreload/modUbuUname.so","ldpreload/modUname.c"])

    print("LD Preload libraries generated")

def updateOS():
    print("Start updating OS containers")
    updateFile = profilePath+"/update"
    #We write the "update" file to inform containers tu update
    subprocess.call(["touch",updateFile])

    #We run the update script in each container
    #to update packages and plugins
    for image in osImages:
        subprocess.call(["sudo","docker","run","-it","-v",profilePath+":/home/blink/profile","--volumes-from","blinkbrowsers",image])
        dockerID = subprocess.check_output(["sudo","docker","ps","-l","-q"])
        subprocess.call(["sudo","docker","commit",dockerID.decode().strip(),image])
        print("Update of "+image+" complete")

    #We remove the update file
    subprocess.call(["rm",updateFile])
    print("OS Containers updated")

def updateBrowsers():
    print("Start updating browsers")

    #We remove the old browser container and image
    subprocess.call(["sudo","docker","rm","blinkbrowsers"])
    subprocess.call(["sudo","docker","rmi","blinkbrowsers"])

    #We build the new image and instantiate it
    buildDockerImage("blinkbrowsers","docker/browsers/")
    instantiateContainer("blinkbrowsers")

    print("Browsers updated")

def writeInstallComplete(mode):
    #######
    # We write a file that indicates that the installation is complete
    # Format of the install complete file
    # data = "XXXX YYYY"
    # data[0] = "XXXX" -> days since the last update of OS containers
    # data[1] = "YYYY" -> days since the last update of browsers
    #######

    data = []

    if mode < 2:
        #We read the current installComplete file
        with open('installComplete', 'r') as f:
            data = f.read().strip().split(" ")
        #We update either the first or second counter
        data[mode] = datetime.date.today().toordinal()
    elif mode == 2:
        # We update both counters
        #(in the case of a fresh install)
        nowDate = datetime.date.today().toordinal()
        data = [nowDate,nowDate]

    if len(data) == 2:
        with open('installComplete', 'w') as f:
            f.write("{} {}".format(data[0],data[1]))
    print("installComplete file written")

def main():

    if not os.path.isfile("installComplete"):
        checkInstallation()
        writeInstallComplete(2)
        print("Installation verified")
    else:
        #We check if the "LD preload" libraries have been compiled in the last 30 days
        #If not, we retrieve the latest version online and recompile the libraries
        with open('installComplete', 'r') as f:
            data = f.read().strip().split(" ")
        pastOSDate = datetime.date.fromordinal(int(data[0]))
        pastBrowsersDate = datetime.date.fromordinal(int(data[1]))
        nowDate = datetime.date.today()
        OSDays = (nowDate-pastOSDate).days
        browsersDays = (nowDate-pastBrowsersDate).days
        print("Days since last OS update : {}".format(OSDays))
        print("Days since last browsers update : {}".format(browsersDays))
        if OSDays > 15:
            updateOS()
            generateLibrairies()
            writeInstallComplete(0)
        if browsersDays > 45:
            writeInstallComplete(1)
            updateBrowsers()

    print("Launching Blink browsing environment")
    launchCommand = "sudo docker run -ti --rm -e DISPLAY " \
                    "-v /tmp/.X11-unix:/tmp/.X11-unix " \
                    "-v "+downloadsPath+":/home/blink/Downloads " \
                    "-v "+profilePath+":/home/blink/profile " \
                    "-v "+ldpreloadPath+":/home/blink/ldpreload "\
                    "--volumes-from blinkbrowsers " \
                    "--volumes-from blinkfonts "
    if len(sys.argv) == 2:
        chosenImage = sys.argv[1]
    else :
        chosenImage = osImages[random.randint(0,len(osImages)-1)]

    #We select the corresponding LD Preload library
    if chosenImage is "blinkfed":
        subprocess.call(["cp","-f","ldpreload/modFedUname.so","ldpreload/modUname.so"])
    else:
        subprocess.call(["cp","-f","ldpreload/modUbuUname.so","ldpreload/modUname.so"])

    print("Image "+chosenImage+" chosen")
    subprocess.call(launchCommand+chosenImage,shell=True)

    print("End of script")

if __name__ == "__main__":
    main()
