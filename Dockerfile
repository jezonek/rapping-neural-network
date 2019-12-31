FROM python:3
WORKDIR /code
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN pip install -r requirements.txt
CMD gunicorn app:app