FROM python:3.8

RUN apt-get -y update && apt-get install -y netcat

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV LISTEN_PORT 8000
EXPOSE 8000

COPY . .
