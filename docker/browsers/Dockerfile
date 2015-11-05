FROM alpine:latest

WORKDIR /home/blink/browsers
ADD /extensions /home/blink/browsers/extensions

#Alpine packages
RUN apk add --update bash wget bzip2 binutils ca-certificates && rm -rf /var/cache/apk/*

#Chrome
RUN mkdir chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN ar vx google-chrome-stable_current_amd64.deb 
RUN tar -C chrome -xJf data.*
RUN bash extensions/nativeApp/install_host.sh

#Firefox
RUN wget -r -l1 -np -nd -A "firefox*.bz2" https://download-installer.cdn.mozilla.net/pub/firefox/releases/latest/linux-x86_64/en-US/
RUN tar -xvjf firefox*
RUN cp extensions/jid1-d1BM58Kj2zuEUg@jetpack.xpi firefox/browser/extensions/
RUN mkdir -p /home/blink/.mozilla/firefox/blink.default
RUN cp extensions/extensions.json /home/blink/.mozilla/firefox/blink.default

#Remove temporary files
RUN rm google-chrome-stable_current_amd64.deb 
RUN rm firefox*.bz2
RUN rm *.gz *.xz *binary

VOLUME /home/blink/browsers
VOLUME /home/blink/.mozilla/firefox
VOLUME /home/blink/.config/google-chrome
VOLUME /etc/opt/chrome/
CMD /bin/sh
