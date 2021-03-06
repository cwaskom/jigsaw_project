FROM python:3.8-buster

RUN apt-get update && \
    apt-get -y install python3-pandas 

WORKDIR /usr/app

COPY ./requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY ./ ./

CMD ["flask", "run", "--host=0.0.0.0"]
