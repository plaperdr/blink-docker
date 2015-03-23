FROM fedora:21

RUN yum localinstall -y --nogpgcheck http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
RUN yum update -y && yum clean all
RUN yum install -y PackageKit-browser-plugin djview4-plugin esteid-browser-plugin freewrl-plugin gnash-plugin gnome-chemistry-utils-mozplugin gnome-shell gxine-mozplugin kopete kpartsplugin lightspark-mozilla-plugin mozplugger npapi-vlc npapi-vlc-gtk nspluginwrapper rhythmbox spice-xpi totem-mozplugin-vegas x2goplugin xine-plugin totem-mozplugin gecko-mediaplayer gnupg2 pinentry-gtk sudo python3 python3-numpy && yum clean all
RUN wget http://dl.google.com/linux/direct/google-talkplugin_current_x86_64.rpm 
RUN yum install -y google-talkplugin_current_x86_64.rpm --nogpgcheck
RUN mv /usr/lib64/mozilla/plugins /usr/lib64/mozilla/plugins.originals
RUN ln -sf /usr/lib64/libudev.so.1 /usr/lib64/libudev.so.0

# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/blink && \
    echo "blink:x:${uid}:${gid}:Blink,,,:/home/blink:/bin/bash" >> /etc/passwd && \
    echo "blink:x:${uid}:" >> /etc/group && \
    echo "blink ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/blink && \
    chmod 0440 /etc/sudoers.d/blink && \
    chown ${uid}:${gid} -R /home/blink

USER blink
ENV HOME /home/blink

RUN mkdir /home/blink/profile/
RUN mkdir /home/blink/ldpreload/
RUN mkdir /home/blink/.fonts/
RUN mkdir /home/blink/.mozilla/
RUN mkdir /home/blink/.mozilla/plugins/

ADD *.py /home/blink/

CMD sudo chown blink -R /home/blink && sudo chmod +x /home/blink/browsers/extensions/nativeApp/ups-host && python3 ~/mainContainer.py
