FROM tensorflow/tensorflow:1.9.0-py3

RUN apt-get update && \
    apt-get install -y ffmpeg
ADD requirements.txt /root/
RUN pip install -r /root/requirements.txt
ADD . /app
WORKDIR /app

ENTRYPOINT python server.py
