FROM alpine:latest

RUN apk add --update tar && rm -rf /var/cache/apk/*
RUN mkdir -p /home/blink/fonts && wget https://github.com/plaperdr/blink-fonts/raw/master/fonts.tar.gz && tar -xf fonts.tar.gz && mv ALL_FONTS/* /home/blink/fonts/ && rm -r ALL_FONTS/ && rm fonts.tar.gz

VOLUME /home/blink/fonts

CMD /bin/sh
