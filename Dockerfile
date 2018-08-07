FROM tensorflow/tensorflow:1.9.0-py3

RUN apt-get update && \
    apt-get install -y ffmpeg
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT python server.py
