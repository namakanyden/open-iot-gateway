FROM theengs/gateway

COPY docker-entrypoint.sh /

# Enable udevd so that plugged dynamic hardware devices show up in our container.
ENV UDEV=1

ENTRYPOINT [ "/docker-entrypoint.sh" ]
CMD [ "/bin/bash", "-ec", "source /opt/venv/bin/activate && exec /opt/venv/start.sh" ]
