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

#Firefox (latest stable and latest ESR)
RUN wget -O firefox.tar.bz2 "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US" && tar -xvjf firefox* && mv firefox firefox-latest && rm firefox.bz2
RUN wget -O firefox-esr.tar.bz2 "https://download.mozilla.org/?product=firefox-esr-latest&os=linux64&lang=en-US" && tar -xvjf firefox-esr.tar.bz2  && mv firefox firefox-latest-esr && rm firefox-esr.tar.bz2
RUN cp extensions/jid1-d1BM58Kj2zuEUg@jetpack.xpi firefox-latest/browser/extensions/ && cp extensions/jid1-d1BM58Kj2zuEUg@jetpack.xpi firefox-latest-esr/browser/extensions/
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
