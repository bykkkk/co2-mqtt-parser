FROM python:3.11-slim

RUN pip install --no-cache-dir paho-mqtt

COPY run.sh /run.sh
COPY parser.py /parser.py

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]