FROM alpine:latest

RUN apk-install --update tar
RUN mkdir -p /home/blink/fonts && wget http://amiunique.irisa.fr/fonts.tar.gz && tar -xf fonts.tar.gz && mv ALL_FONTS/* /home/blink/fonts/ && rm -r ALL_FONTS/ && rm fonts.tar.gz

VOLUME /home/blink/fonts

CMD /bin/sh
