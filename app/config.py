import os
from dotenv import load_dotenv
from kombu import Exchange, Queue
from celery.schedules import crontab

load_dotenv(dotenv_path='.env')
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', '123456')
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASK_SQLALCHEMY_DATABASE_URI',
                                             'mysql+cymysql://root:mysql@127.0.0.1:3306/atfield')
    CELERY_BROKEN_URL = os.environ.get('FLASK_CELERY_BROKER_URL',
                                       'amqp://guest:guest@127.0.0.1:5672/atfield')
    CELERY_RESULT_BACKEND = os.environ.get('FLASK_CELERY_BROKER_URL',
                                           'redis://:@127.0.0.1:6379/0')
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN_EXPIRATION = 30 * 24 * 3600

    CELERY_INCLUDES = ('scanner',)
    CELERY_IMPORTS = ('scanner',)

    CELERY_QUEUES = (
        Queue('master', Exchange('master'),
              routing_key='master'),
        Queue('node', Exchange('node'),
              routing_key='node'),
    )
    # 路由
    CELERY_ROUTES = {
        'master_*': {
            'queue': 'master',
            'routing_key': 'master'
        },
        'scanner.master.*': {
            'queue': 'master',
            'routing_key': 'master'
        },
        'scanner.node.*': {
            'queue': 'node',
            'routing_key': 'node'
        },
    }

    CELERY_TIMEZONE = 'Asia/Shanghai'

    CELERYBEAT_SCHEDULE = {
        'master_daily_handle': {
            'task': 'master_daily_handle',
            'schedule': crontab(hour=22, minute=23),
        },
    }


config = Config
