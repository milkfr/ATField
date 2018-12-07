#!/bin/bash

source venv/bin/activate

exec celery -A celery_worker.celery worker --loglevel=info -Q task_domain_resolution -n worker_domain_resolution
