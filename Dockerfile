FROM python:3.7.6-alpine3.11

RUN pip install --upgrade pip

RUN mkdir /app

WORKDIR /app

ADD . .

RUN pip install -r requirements.txt

CMD gunicorn app:app --bind 0.0.0.0:$PORT -w 2 --reload --access-logfile - 
