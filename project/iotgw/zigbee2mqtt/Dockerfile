FROM koenkk/zigbee2mqtt

COPY entrypoint.sh /
COPY configuration.yaml /app/data/

ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "/sbin/tini", "--", "node", "index.js" ]
