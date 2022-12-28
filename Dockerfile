# syntax=docker/dockerfile:1
FROM python:latest
RUN apt update && apt install python3-dev gcc -y
RUN useradd -rm -d /home/appuser -s /bin/bash -g root -G sudo -u 1001 appuser
COPY requirements.txt /home/appuser/requirements.txt
COPY entrypoint.sh /home/appuser/entrypoint.sh
RUN chmod +x /home/appuser/entrypoint.sh
USER appuser
WORKDIR /home/appuser
RUN pip3 install -r requirements.txt
ENV PATH=/home/appuser/.local/bin:$PATH
COPY webhookfromghost.ini /home/appuser/webhookfromghost.ini
COPY webhookfromghost.py /home/appuser/webhookfromghost.py
COPY wsgi.py /home/appuser/wsgi.py
EXPOSE 5000/tcp
ENTRYPOINT ["/home/appuser/entrypoint.sh"]
