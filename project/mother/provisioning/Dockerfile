FROM alpine:3.20

LABEL author "mirek"

# Environment variables substitution for Go:  https://github.com/a8m/envsubst
RUN set -o errexit \
    && apk add \
        jo \
        yq \
        jq \
        bash \
        mosquitto \
        curl \
    && machine=$(uname --machine | sed 's/aarch64/arm64/') \
    && curl -L https://github.com/a8m/envsubst/releases/download/v1.2.0/envsubst-$(uname --kernel-name)-"${machine}" --output /usr/local/bin/envsubst \
    && chmod +x /usr/local/bin/envsubst

COPY app/ /app/

WORKDIR /app

CMD [ "/bin/bash", "init.bash" ]
