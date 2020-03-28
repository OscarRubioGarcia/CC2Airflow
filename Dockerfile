FROM alpine:3.10

MAINTAINER Oscar Rubio Garcia 

WORKDIR /code
ENV PORT="DEFAULT"

RUN apk update && apk upgrade && apk add py-pip linux-headers python3==3.6 py3-virtualenv python-dev bash

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN rm -rf requirements.txt

COPY tasks.py app.py function.py humidity.csv temperature.csv tests /code/

RUN addgroup -S dockergroup && adduser -S dockeruser -G dockergroup -h /code
USER dockeruser

CMD invoke runGunicorn -p ${PORT}