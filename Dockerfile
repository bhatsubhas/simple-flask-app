FROM python:3.9.3-slim-buster

RUN pip install --upgrade pip

RUN mkdir /app

WORKDIR /app

ADD requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

ADD . /app

CMD gunicorn app:app --bind 0.0.0.0:80 -w 2 --reload --access-logfile - 

EXPOSE 80


