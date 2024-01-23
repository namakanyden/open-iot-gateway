FROM eclipse-mosquitto

COPY mosquitto.conf /mosquitto/config/
COPY docker-entrypoint.sh /app/

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]

CMD [ "/usr/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf" ]
