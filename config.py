import os
from dotenv import load_dotenv
from kombu import Exchange, Queue
from datetime import timedelta
from celery.schedules import crontab

load_dotenv(dotenv_path=".flaskenv")
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    BASEDIR = basedir
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "hard to guess string")
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("FLASK_DATABASE_URI",
                                             "sqlite:///"+os.path.join(basedir, "data-dev.sqlite"))
    CELERY_BROKER_URL = os.environ.get("FLASK_CELERY_BROKER_URL")

    CELERY_INCLUDES = ("workers",)

    CELERY_QUEUES = (
        Queue("task_result_save", Exchange("task_result_save"),
              routing_key="task_result_save"),
        Queue("task_domain_resolution", Exchange("task_domain_resolution"),
              routing_key="task_domain_resolution"),
        Queue("task_port_monitor", Exchange("task_port_monitor"),
              routing_key="task_port_monitor"),
        Queue("task_awvs", Exchange("task_awvs"),
              routing_key="task_awvs"),
    )
    # # 路由
    CELERY_ROUTES = {
        "workers.result.save": {
            "queue": "task_result_save",
            "routing_key": "task_result_save"
        },
        "workers.domain_resolution.worker": {
            "queue": "task_domain_resolution",
            "routing_key": "task_domain_resolution"
        },
        "workers.port_monitor.worker": {
            "queue": "task_port_monitor",
            "routing_key": "task_port_monitor"
        },
        "workers.awvs.worker": {
            "queue": "task_awvs",
            "routing_key": "task_awvs"
        }
    }

    CELERY_TIMEZONE = "Asia/Shanghai"

    CELERYBEAT_SCHEDULE = {
        "domain_resolution_schedule": {
            "task": "workers.domain_resolution.worker",
            "schedule": crontab(hour=4, minute=0),
            # "schedule": timedelta(seconds=10),
            "kwargs": {"targets": ""},
        },
        "port_monitor_schedule": {
            "task": "workers.port_monitor.worker",
            "schedule": crontab(hour=4, minute=0, day_of_week=4),
            # "schedule": timedelta(seconds=10),
            "kwargs": {"targets": "", "options": "-n -Pn -sT -p1-65535"},
        },
        "awvs_schedule": {
            "task": "workers.awvs.worker",
            "schedule": crontab(hour=4, minute=0, day_of_month=1),
            # "schedule": timedelta(seconds=10),
            "kwargs": {"targets": "127.0.0.1:8088", "options": "do scan"},
        },
    }

    @staticmethod
    def init_app(app):
        pass


config = Config
