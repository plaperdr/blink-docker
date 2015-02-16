FROM gliderlabs/alpine:3.1

WORKDIR /home/blink/browsers
ADD /extensions /home/blink/browsers/extensions

#wget
RUN apk-install --update bash wget bzip2 binutils

#Chrome
RUN mkdir chrome
RUN wget --no-check-certificate https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb 
RUN ar vx google-chrome-stable_current_amd64.deb 
RUN lzma -cd data.tar.lzma | tar xvf - -C chrome
RUN bash extensions/nativeApp/install_host.sh

#Firefox
RUN wget -r -nd ftp://ftp.mozilla.org/pub/mozilla.org/firefox/releases/latest/linux-x86_64/en-US/*
RUN bzip2 -cd firefox* | tar xvf -
RUN cp extensions/jid1-d1BM58Kj2zuEUg@jetpack.xpi firefox/browser/extensions/
RUN mkdir -p /home/blink/.mozilla/firefox/blink.default
RUN cp extensions/extensions.json /home/blink/.mozilla/firefox/blink.default

#Remove temporary files
RUN rm google-chrome-stable_current_amd64.deb 
RUN rm firefox*.bz2
RUN rm *.gz *.lzma *binary

VOLUME /home/blink/browsers
VOLUME /home/blink/.mozilla/firefox
VOLUME /home/blink/.config/google-chrome
VOLUME /etc/opt/chrome/
CMD /bin/sh
