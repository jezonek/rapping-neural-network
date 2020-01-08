FROM python:3.6
#FROM tensorflow/tensorflow:latest
#FROM tiangolo/meinheld-gunicorn:python3.7
ENV PYTHONUNBUFFERED 1
ENV MODULE_NAME app
#RUN mkdir /app
WORKDIR /app

COPY requirements-webapp.txt /app/
RUN pip3 install -r requirements-webapp.txt
