FROM telegraf:1.31

RUN apt update \
    && apt install --yes python3 python-is-python3 python3-pip \
    && pip3 install --break-system-packages pydantic line-protocol-parser

