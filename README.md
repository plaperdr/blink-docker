# Blink + Docker = :heart: #

### Disclaimer ###
This tool is experimental and still in development. Feel free to post any issues you encounter so that we can squash the remaining bugs that are hiding. Any suggestions or any improvement ideas are welcome to make Blink with Docker a better and more stable tool.

### Requirements ###
**Docker**, **Python 3** and **gcc** are needed to build Blink.  

**Python 3 and gcc**  
For Fedora: `sudo yum install python3 gcc`  
For Ubuntu/Debian: `sudo apt-get install python3 gcc`  

**Docker**  
For Fedora: [Link](https://docs.docker.com/installation/fedora/)  
For Debian: [Link](https://docs.docker.com/installation/debian/)  
For Ubuntu: [Link](https://docs.docker.com/installation/ubuntulinux/)  

It is recommended to have at least **6GB** of free hard drive space to install every Blink components.

### Quick install ###
If you want to try Blink, here are 4 simple commands to get it running:
```
git clone https://github.com/plaperdr/blink-docker.git
cd blink-docker/
python3 downloadFromHub.py
python3 run.py
```
### Installation ###
The **downloadFromHub.py** script is now the recommended method of installation. It downloads the main images directly from Docker Hub.
You can also run the **installContainers.py** script to build Blink from scratch. The process can take some time depending on your internet connection (download of packages, fonts and plugins).

### Running ###
Run the **run.py** and it will launch a browsing platform on the fly in a matter of seconds. During its first launch, the script checks if the installation was correct, builds the final Docker images and generates two C librairies. If the script encounters any problems during this first run, go through the complete installation process again and retry.

### Windows and MacOS support ###
While Windows and MacOS are not officially supported yet, it should be possible to run Blink on these platforms via a Linux virtual machine with VirtualBox or VMWare.  
It should be noted that we may investigate the use of Boot2Docker in the future to improve performances.

### Docker images and containers ###

4 images are downloaded from Docker Hub (or can be built from scratch)
* [plaperdr/blinkubuorig](https://hub.docker.com/r/plaperdr/blinkubuorig/)
* [plaperdr/blinkfedorig](https://hub.docker.com/r/plaperdr/blinkfedorig/)
* [plaperdr/blinkbrowsers](https://hub.docker.com/r/plaperdr/blinkbrowsers/)
* [plaperdr/blinkfonts](https://hub.docker.com/r/plaperdr/blinkfonts/)

2 images are built locally during the installation
* blink/blinkUbu
* blink/blinkFed

2 containers are created during installation
* blinkfonts
* blinkbrowsers
