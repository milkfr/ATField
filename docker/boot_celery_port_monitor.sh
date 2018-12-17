#!/bin/bash

source venv/bin/activate

exec celery -A celery_worker.celery worker --loglevel=info -Q task_port_monitor -n worker_port_monitor
