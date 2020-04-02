FROM python:3.6-slim

MAINTAINER Oscar Rubio Garcia 

WORKDIR /code
ENV PORT="DEFAULT"

RUN apt-get update && apt-get upgrade && apt-get install -y \
        build-essential \
        make \
        gcc \
        bash g++

RUN pip install --no-cache-dir numpy cython 
RUN pip install --no-cache-dir scipy
RUN pip install --no-cache-dir scikit-learn
RUN pip install --no-cache-dir pandas

COPY requirements-img.txt requirements.txt
RUN pip install -r requirements.txt
RUN rm -rf requirements.txt

COPY tasks.py app.py function.py humidity.csv temperature.csv tests /code/

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]