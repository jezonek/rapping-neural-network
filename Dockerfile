FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV MODULE_NAME app
RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt
