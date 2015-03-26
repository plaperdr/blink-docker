#!/usr/bin/python3
# -*-coding:utf-8 -*

import os
import subprocess

############### Main
def main():
    print("Blink Update script")

    #We update packages using the package manager
    ret = subprocess.call(["sudo","apt-get","update"])
    if ret != 0:
        print("Error while updating")
    ret = subprocess.call(["sudo","apt-get","upgrade","-y"])
    if ret != 0:
        print("Error while upgrading")
    ret = subprocess.call(["sudo","apt-get","clean"])
    if ret != 0:
        print("Error while cleaning packages")

    for dirpath, dirnames, files in os.walk('/usr/lib/mozilla/plugins/'):
        if files:
            #We move new plugins if they were updated and we overwrite the old one
            subprocess.call(["sudo","mv","-f","/usr/lib/mozilla/plugins/*", "/home/blink/plugins/"])

if __name__ == "__main__":
    main()