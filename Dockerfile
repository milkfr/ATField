FROM python:3.6

RUN useradd -d /home/flask -m -s /bin/bash flask -p flask
WORKDIR /home/flask
USER flask

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn gevent

COPY app app
COPY migrations migrations
COPY workers workers
COPY wsgi.py config.py celery_worker.py boot.sh .flaskenv ./

# run-time configuration
EXPOSE 8080
ENTRYPOINT ["./boot.sh"]