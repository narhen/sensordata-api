from debian:jessie

RUN useradd --user-group --create-home --shell /bin/bash api

ENV HOME=/home/api
RUN chown -R api:api $HOME

RUN apt-get update
RUN apt-get install --yes python2.7 python2.7-dev python-pip libpq-dev libffi-dev

USER api
RUN mkdir $HOME/sensordataapi
COPY . $HOME/sensordataapi/

user root
RUN pip install --upgrade -r $HOME/sensordataapi/requirements.txt
RUN rm $HOME/sensordataapi/Dockerfile
RUN rm $HOME/sensordataapi/run.sh
RUN rm $HOME/sensordataapi/requirements.txt

user api
WORKDIR $HOME/sensordataapi
CMD ["./app.py"]

