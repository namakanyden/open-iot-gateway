FROM telegraf

RUN apt update \
    && apt install --yes python3 python-is-python3 python3-pip pydantic \
    && pip3 install --break-system-packages line-protocol-parser
