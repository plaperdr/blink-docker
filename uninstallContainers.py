#!/usr/bin/python3
# -*-coding:utf-8 -*

from installUtils import *

containers = ["blinkbrowsers","blinkfonts","torproxy"]
localImages = [prefixRepoLocal+name for name in ["blinkfed","blinkubu"]]
remoteImages = [prefixRepoHub+name for name in dockerImages]

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def main():
    print("Blink uninstallation script")
    if query_yes_no("Do you want to uninstall Blink?"):
        print("Removing existing containers")
        for container in containers:
            removeContainer(container)

        print("Removing existing images")
        for image in localImages:
            removeImage(image)
        for image in remoteImages:
            removeImage(image+":exp")

        print("Uninstallation of Blink containers complete")
    else:
        print("Uninstallation aborted")



if __name__ == "__main__":
    main()