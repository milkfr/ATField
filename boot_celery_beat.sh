#!/bin/bash

source venv/bin/activate


exec celery beat -A celery_worker.celery -l INFO
