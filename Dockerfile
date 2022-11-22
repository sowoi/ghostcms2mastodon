# syntax=docker/dockerfile:1
FROM python:3.8-slim-bullseye
RUN apt update && apt install python3-dev gcc -y
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY webhookfromghost.ini webhookfromghost.ini
COPY webhookfromghost.py webhookfromghost.py
COPY wsgi.py wsgi.py
EXPOSE 5000/tcp
CMD [ "uwsgi", "--ini", "webhookfromghost.ini" ]
