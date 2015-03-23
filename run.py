#!/usr/bin/python3
# -*-coding:utf-8 -*

import re
import os
import sys
import random
import datetime
import subprocess
import urllib.request

osImages = ["blinkfed","blinkubu"]
ubuntuName = "trusty"
fedoraName = "fc21"

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

    #We write a file that indicates that the installation is complete
    #This file contains the date of last generation
    with open('installComplete', 'w') as f:
            f.write(str(datetime.date.today().toordinal()))
    print("installComplete file written")

def main():

    if not os.path.isfile("installComplete"):
        checkInstallation()
        print("Installation verified")
    else:
        #We check if the "LD preload" libraries have been compiled in the last 30 days
        #If not, we retrieve the latest version online and recompile the libraries
        with open('installComplete', 'r') as f:
            data = f.read()
        pastDate = datetime.date.fromordinal(int(data))
        nowDate = datetime.date.today()
        days = (nowDate-pastDate).days
        print("Days since last library regeneration : {}".format(days))
        if days > 30:
            generateLibrairies()

    print("Launching Blink browsing environment")
    downloadsPath =  os.path.abspath("data/downloads")
    profilePath = os.path.abspath("data/profile")
    ldpreloadPath = os.path.abspath("ldpreload")
    launchCommand = "sudo docker run -ti --rm -e DISPLAY " \
                    "-v /tmp/.X11-unix:/tmp/.X11-unix " \
                    "-v "+downloadsPath+":/home/blink/Downloads " \
                    "-v "+profilePath+":/home/blink/profile " \
                    "-v "+ldpreloadPath+":/home/blink/ldpreload "\
                    "--volumes-from blinkbrowsers " \
                    "--volumes-from blinkplugins " \
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
