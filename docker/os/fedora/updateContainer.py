#!/usr/bin/python3
# -*-coding:utf-8 -*

import os
import subprocess

############### Main
def main():
    print("Blink Update script")

    #We update packages using the package manager
    ret = subprocess.call(["sudo","yum","update","-y"])
    if ret != 0:
        print("Error while updating")
    ret = subprocess.call(["sudo","yum","clean","all"])
    if ret != 0:
        print("Error while cleaning packages")

    for dirpath, dirnames, files in os.walk('/usr/lib64/mozilla/plugins/'):
        if files:
            #We move new plugins if they were updated and we overwrite the old one
            subprocess.call(["sudo","mv","-f","/usr/lib64/mozilla/plugins/*", "/home/blink/plugins/"])

if __name__ == "__main__":
    main()