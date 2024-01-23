FROM ghcr.io/gethomepage/homepage:latest

COPY config /app/config
COPY images /app/public/images
COPY docker-entrypoint.sh /app

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["node", "server.js"]
