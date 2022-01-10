FROM ubuntu:20.04
FROM python:3.8
MAINTAINER maria.blanco4@alu.uclm.es  

RUN apt-get update 

RUN apt-get install sqlite3

RUN apt-get update && apt-get install -y \
    python3-pip

RUN apt-get update && apt-get install -y python3-opencv

COPY requirements.txt ./requirements.txt
WORKDIR ./
RUN pip install -r requirements.txt
RUN apt-get update
COPY . ./