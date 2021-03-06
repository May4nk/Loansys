FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./requirement.txt  /app/

RUN pip3 install -r requirement.txt

COPY . /app 

