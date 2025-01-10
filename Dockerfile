FROM python:3.12-slim

RUN apt-get update && apt-get install -y git nginx

COPY app /app
WORKDIR /app
RUN pip install -r requirements.txt

COPY nginx.conf /etc/nginx/nginx.conf

CMD ["/bin/sh", "./run.sh"]
