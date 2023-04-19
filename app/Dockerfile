FROM python:3.11.3-alpine3.17

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip3 install --upgrade pip -r requirements.txt
RUN mkdir storage

COPY . /app

EXPOSE 8080