import os
from dotenv import load_dotenv
from kombu import Exchange, Queue
from datetime import timedelta

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
    ELASTICSEARCH_HOST = os.environ.get("FLASK_ELASTICSEARCH_HOST", "localhost:9200")
    # CELERY_RESULT_BACKEND = os.environ.get("FLASK_CELERY_RESULT_BACKEND")
    CELERY_BROKER_URL = os.environ.get("FLASK_CELERY_BROKER_URL")

    CELERY_QUEUES = (
        Queue("task_result_save", Exchange("task_result_save"),
              routing_key="task_result_save"),
        Queue("task_domain_resolution", Exchange("task_domain_resolution"),
              routing_key="task_domain_resolution"),
        Queue("task_port_scan_quick", Exchange("task_port_scan_quick"),
              routing_key="task_port_scan_quick"),
        Queue("task_port_scan_slow", Exchange("task_port_scan_slow"),
              routing_key="task_port_scan_slow")
    )
    # # 路由
    CELERY_ROUTES = {
        "workers.result.save": {"queue": "task_result_save",
                                "routing_key": "task_result_save"},
        "workers.domain_resolution.worker": {"queue": "task_domain_resolution",
                                             "routing_key": "task_domain_resolution"},
        "workers.port_scan_quick.worker": {"queue": "task_port_scan_quick",
                                           "routing_key": "task_port_scan_quick"},
        "workers.port_scan_slow.worker": {"queue": "task_port_scan_slow",
                                          "routing_key": "task_port_scan_slow"},
    }

    CELERY_TIMEZONE = "UTC"

    CELERYBEAT_SCHEDULE = {
        "domain_resolution_schedule": {
            "task": "workers.domain_resolution.worker",
            "schedule": timedelta(seconds=60),
            "kwargs": {"targets": ""},
        },
        "port_scan_quick_scheduler": {
            "task": "workers.port_scan_quick.worker",
            "schedule": timedelta(seconds=60),
            "kwargs": {"targets": "-p1-5000 --rate 1000"},
        },
        "port_scan_slow_scheduler": {
            "task": "worker.port_scan_slow.worker",
            "schedule": timedelta(seconds=60),
            "kwargs": {"targets": "-n -Pn -sT -p 1-5000"},
        }
    }

    @staticmethod
    def init_app(app):
        pass


config = Config
