#!/bin/bash

source venv/bin/activate

exec celery -A celery_worker.celery worker --loglevel=info -Q task_result_save -n worker_result_save
