FROM alpine:latest

WORKDIR /home/blink/browsers
ADD /extensions /home/blink/browsers/extensions

#Alpine packages
RUN apk add --update bash wget bzip2 binutils ca-certificates && rm -rf /var/cache/apk/*

#Chrome
RUN mkdir chrome && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && ar vx google-chrome-stable_current_amd64.deb && tar -C chrome -xJf data.* && rm google-chrome-stable_current_amd64.deb *.gz *.xz *binary && bash extensions/nativeApp/install_host.sh
RUN mkdir -p /home/blink/.config/google-chrome/Default && mkdir -p /home/blink/.config/chromium/Default

#Opera
RUN mkdir opera && wget -Oopera.deb 'http://www.opera.com/download/get/?id=38856&location=395&nothanks=yes&sub=marine' && ar vx opera.deb && tar -C opera -xJf data.* && rm opera.deb *.gz *.xz *binary

#Firefox (latest stable and latest ESR)
RUN wget -O firefox.tar.bz2 "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US" && tar -xvjf firefox* && mv firefox firefox-latest && rm firefox.tar.bz2
RUN wget -O firefox-esr.tar.bz2 "https://download.mozilla.org/?product=firefox-esr-latest&os=linux64&lang=en-US" && tar -xvjf firefox-esr.tar.bz2  && mv firefox firefox-latest-esr && rm firefox-esr.tar.bz2
RUN cp extensions/jid1-d1BM58Kj2zuEUg@jetpack.xpi firefox-latest/browser/extensions/ && cp extensions/jid1-d1BM58Kj2zuEUg@jetpack.xpi firefox-latest-esr/browser/extensions/
RUN mkdir -p /home/blink/.mozilla/firefox/blink.default && cp extensions/extensions.json /home/blink/.mozilla/firefox/blink.default

VOLUME /home/blink/browsers /home/blink/.mozilla/firefox /home/blink/.config/ /etc/opt/chrome/ /etc/chromium
CMD /bin/sh
