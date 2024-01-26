FROM alpine

LABEL author "mirek"

RUN apk add jo yq jq bash envsubst mosquitto

COPY bin/init.bash /
COPY templates/ /templates/
# COPY local.env /

CMD [ "/init.bash" ]
