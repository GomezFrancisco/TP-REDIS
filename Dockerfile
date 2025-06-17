FROM python:3.12-slim

WORKDIR /api
COPY api/ .

RUN pip3 install flask redis

EXPOSE 5000