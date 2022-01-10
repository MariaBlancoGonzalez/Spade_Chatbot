FROM ubuntu:20.04
MAINTAINER maria.blanco4@alu.uclm.es  

RUN apt-get update 

CMD [“echo”,”Image created”] 

RUN apt-get install python3.8.10
RUN apt-get install sqlite3

COPY requirements.txt ./requirements.txt
WORKDIR ./
RUN pip install -r requirements.txt
RUN apt-get update
COPY . ./