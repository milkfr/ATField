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
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get("FLASK_MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("FLASK_MAIL_PASSWORD")
    MAIL_SUBJECT_PREFIX = "[milkfr]"
    MAIL_SENDER = os.environ.get("FLASK_MAIL_USERNAME")

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("FLASK_DATABASE_URI",
                                             "sqlite:///"+os.path.join(basedir, "data-dev.sqlite"))
    ELASTICSEARCH_HOST = os.environ.get("FLASK_ELASTICSEARCH_HOST", "localhost:9200")
    # CELERY_RESULT_BACKEND = os.environ.get("FLASK_CELERY_RESULT_BACKEND")
    CELERY_BROKER_URL = os.environ.get("FLASK_CELERY_BROKER_URL")

    CELERY_QUEUES = (
    #     # Queue("default", Exchange("default"), routing_key="default"),
        Queue("task_result_save", Exchange("task_result_save"),
              routing_key="task_result_save"),
        Queue("task_domain_resolution", Exchange("task_domain_resolution"),
              routing_key="task_domain_resolution"),
    #     Queue("task_port_scan_quick", Exchange("task_port_scan_quick"),
    #           routing_key="task_port_scan_quick"),
    #     Queue("task_port_scan_slow", Exchange("task_port_scan_slow"),
    #           routing_key="task_port_scan_slow")
    )
    # # 路由
    CELERY_ROUTES = {
        "workers.result.save": {"queue": "task_result_save",
                                "routing_key": "task_result_save"},
        "workers.domain_resolution.worker": {"queue": "task_domain_resolution",
                                                      "routing_key": "task_domain_resolution"},
        # "workers.port_scan_quick.worker": {"queue": "task_port_scan_quick",
        #                                                      "routing_key": "task_port_scan_quick"},
        # "workers.port_scan_slow.worker": {"queue": "task_port_scan_slow",
        #                                                   "routing_key": "task_port_scan_slow"},
    }

    CELERY_TIMEZONE = "UTC"

    CELERYBEAT_SCHEDULE = {
        "taskA_schedule": {
            "task": "workers.domain_resolution.worker",
            "schedule": timedelta(seconds=60),
            "kwargs": {"targets": ""},
        },
        # 'taskB_scheduler': {
        #     "task": "workers.port_scan_quick.worker",
        #     "schedule": timedelta(seconds=6),
        #     "kwargs": {"targets": "-p1-5000 --rate 1000"},
        # },
        # 'add_schedule': {
        #     "task": "worker.port_scan_slow.worker",
        #     "schedule": timedelta(seconds=6),
        #     "kwargs": {"targets": "-n -Pn -sT -p 1-5000"},
        # }
    }

    @staticmethod
    def init_app(app):
        pass


config = Config
