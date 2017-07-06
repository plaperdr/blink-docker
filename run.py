#!/usr/bin/python3
# -*-coding:utf-8 -*

import re
import os
import sys
import random
import datetime
import subprocess
import urllib.request
from installContainers import buildDockerImageLocal,instantiateContainer
from installUtils import prefixRepoLocal,prefixRepoHub

osImages = ["blinkfed","blinkubu"]
ubuntuName = "xenial"
fedoraName = "fc25"

downloadsPath =  os.path.abspath("data/downloads")
profilePath = os.path.abspath("data/profile")
ldpreloadPath = os.path.abspath("ldpreload")
seccompPath = os.path.abspath("seccomp/chrome.json")
timezonePath = "/usr/share/zoneinfo/"

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

def getRandomTimezone():
    timezone = []
    for path, subdirs, files in os.walk(timezonePath):
        for name in files:
            timezone.append(os.path.join(path, name)[len(timezonePath):])
    timezone = [t for t in timezone if "posix" not in t and "right" not in t and ".tab" not in t]
    return timezone[random.randint(0,len(timezone)-1)]

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
    ubuSource = urllib.request.urlopen("https://packages.ubuntu.com/"+ubuntuName+"/linux-image-generic").read()
    ubuKernel = re.search("linux-image-([\.\w-]*?)-generic",str(ubuSource)).group(1)+"-generic"
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
        subprocess.call(["sudo","docker","run","-it","-v",profilePath+":/home/blink/profile","--volumes-from","blinkbrowsers",prefixRepoLocal+image])
        dockerID = subprocess.check_output(["sudo","docker","ps","-l","-q"])
        subprocess.call(["sudo","docker","commit",dockerID.decode().strip(),prefixRepoLocal+image])
        print("Update of "+image+" complete")

    #We remove the update file
    subprocess.call(["rm",updateFile])
    print("OS Containers updated")

def updateBrowsers():
    print("Start updating browsers")

    #We remove the old browser container and image
    subprocess.call(["sudo","docker","rm","-v","blinkbrowsers"])
    subprocess.call(["sudo","docker","rmi","blinkbrowsers"])

    #We build the new image and instantiate it
    buildDockerImageLocal("blinkbrowsers","docker/browsers/")
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

def startTorProxy():
    subprocess.call(["sudo","docker","start","torproxy"])

def stopTorProxy():
    subprocess.call(["sudo","docker","stop","torproxy"])

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

    if len(sys.argv) == 2:
        chosenImage = sys.argv[1]
    else :
        chosenImage = osImages[random.randint(0,len(osImages)-1)]
    print("Image " + chosenImage + " chosen")

    chosenTimezone = getRandomTimezone()
    print(chosenTimezone+" timezone chosen")

    print("Launching Blink browsing environment")
    launchCommand = "sudo docker run -ti --rm -e DISPLAY " \
                    "-v /tmp/.X11-unix:/tmp/.X11-unix " \
                    "-v "+downloadsPath+":/home/blink/Downloads:z " \
                    "-v "+profilePath+":/home/blink/profile:z " \
                    "-v "+ldpreloadPath+":/home/blink/ldpreload:z " \
                    "--volumes-from blinkbrowsers " \
                    "--volumes-from blinkfonts " \
                    "--device /dev/snd " \
                    "-v /run/user/`id -u`/pulse/native:/run/user/`id -u`/pulse/native " \
                    "-v /dev/shm:/dev/shm " \
                    "-v /etc/machine-id:/etc/machine-id " \
                    "-v /var/lib/dbus:/var/lib/dbus " \
                    "--security-opt seccomp:"+seccompPath+" " \
                    "--net container:torproxy " \
                    "-e TZ="+chosenTimezone+" "+prefixRepoLocal

    #We select the corresponding LD Preload library
    if chosenImage is "blinkfed":
        subprocess.call(["cp","-f","ldpreload/modFedUname.so","ldpreload/modUname.so"])
    else:
        subprocess.call(["cp","-f","ldpreload/modUbuUname.so","ldpreload/modUname.so"])

    #Start Tor proxy
    startTorProxy()
    subprocess.call(launchCommand+chosenImage,shell=True)

    #When browsing is finished, we stop the Tor proxy container
    stopTorProxy()

    print("End of script")

if __name__ == "__main__":
    main()
