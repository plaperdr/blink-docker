FROM blinkubuorig

# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    echo "blink:x:${uid}:${gid}:Blink,,,:/home/blink:/bin/bash" >> /etc/passwd && \
    echo "blink:x:${uid}:" >> /etc/group && \
    echo "blink ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/blink && \
    chmod 0440 /etc/sudoers.d/blink && \
    chown ${uid}:${gid} -R /home/blink

USER blink
ENV HOME /home/blink

CMD sudo chown blink -R /home/blink && sudo chmod +x /home/blink/browsers/extensions/nativeApp/ups-host && python3 ~/mainContainer.py
