FROM fedora:23

RUN dnf install -y --nogpgcheck http://linuxdownload.adobe.com/adobe-release/adobe-release-x86_64-1.0-1.noarch.rpm
RUN dnf install --nogpgcheck http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
RUN dnf update -y && dnf clean all
RUN dnf install -y PackageKit-browser-plugin djview4-plugin firefox-esteid-plugin freewrl-plugin gnash-plugin gnome-chemistry-utils-mozplugin gnome-shell gxine-mozplugin kopete kpartsplugin mozplugger npapi-vlc npapi-vlc-gtk nspluginwrapper rhythmbox spice-xpi x2goplugin xine-plugin  gecko-mediaplayer gnupg2 pinentry-gtk sudo python3 python3-numpy flash-plugin && dnf clean all
RUN wget http://dl.google.com/linux/direct/google-talkplugin_current_x86_64.rpm 
RUN dnf install -y google-talkplugin_current_x86_64.rpm --nogpgcheck
RUN ln -sf /usr/lib64/libudev.so.1 /usr/lib64/libudev.so.0

RUN mkdir -p /home/blink/profile/
RUN mkdir /home/blink/ldpreload/
RUN mkdir /home/blink/.fonts/
RUN mkdir -p /home/blink/.mozilla/plugins/
RUN mkdir /home/blink/plugins/
RUN mv /usr/lib64/mozilla/plugins/* /home/blink/plugins/

RUN dnf install -y tar && wget http://amiunique.irisa.fr/fontsFedora.tar.gz && tar -C /usr/share/fonts/ -xf fontsFedora.tar.gz && rm fontsFedora.tar.gz
ADD ubuntu/scripts/*.py /home/blink/
ADD updateContainer.py /home/blink/
ADD pluginsWeightBlink.csv /home/blink/
ADD ubuntu/scripts/fontsWeightBlink.csv /home/blink/
