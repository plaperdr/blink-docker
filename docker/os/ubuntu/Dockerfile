FROM ubuntu:14.10

RUN apt-get update && apt-get install -y wget djview-plugin browser-plugin-gnash browser-plugin-lightspark browser-plugin-packagekit browser-plugin-spice browser-plugin-vlc gxineplugin kopete-plugin-thinklight kpartsplugin mozplugger rhythmbox-mozilla totem-mozilla x2goplugin xine-plugin gecko-mediaplayer gnupg2 sqlite3 libpango1.0-0 sudo python3 python3-numpy libnss3 && apt-get clean
RUN wget https://dl.google.com/linux/direct/google-talkplugin_current_amd64.deb
RUN dpkg -i google-talkplugin_current_amd64.deb
RUN sudo ln -sf /lib/x86_64-linux-gnu/libudev.so.1 /usr/lib/libudev.so.0
RUN rm -rf /usr/share/mozilla/extensions/*

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
RUN mkdir /home/blink/plugins/
RUN sudo mv /usr/lib/mozilla/plugins/* /home/blink/plugins/

ADD *.py /home/blink/
ADD fontsOS/fontsUbuntu/* /usr/share/fonts/

CMD sudo chown blink -R /home/blink && sudo chmod +x /home/blink/browsers/extensions/nativeApp/ups-host && python3 ~/mainContainer.py
