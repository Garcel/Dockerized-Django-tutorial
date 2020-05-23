FROM python:3.8.3-alpine

ARG DJANGO_ENV

ENV PYTHONUNBUFFERED=1
ENV WEBAPP_DIR=/webapp

RUN mkdir $WEBAPP_DIR

WORKDIR $WEBAPP_DIR

ADD requirements/base.txt $WEBAPP_DIR/
ADD requirements/${DJANGO_ENV}.txt $WEBAPP_DIR/

RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r ${DJANGO_ENV}.txt

ADD . $WEBAPP_DIR/