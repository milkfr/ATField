import os
from dotenv import load_dotenv
from kombu import Exchange, Queue
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
    CELERY_IMPORTS = ("workers",)

    CELERY_QUEUES = (
        Queue("task_result_save", Exchange("task_result_save"),
              routing_key="task_result_save"),
        Queue("task_domain_resolution", Exchange("task_domain_resolution"),
              routing_key="task_domain_resolution"),
        Queue("task_port_monitor", Exchange("task_port_monitor"),
              routing_key="task_port_monitor"),
        Queue("task_amqp", Exchange("task_amqp"),
              routing_key="task_amqp"),
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
        "workers.amqp.worker": {
            "queue": "task_amqp",
            "routing_key": "task_amqp"
        }
    }

    CELERY_TIMEZONE = "Asia/Shanghai"

    CELERYBEAT_SCHEDULE = {
        "domain_resolution_schedule": {
            "task": "workers.domain_resolution.worker",
            "schedule": crontab(hour=0, minute=0),
            "kwargs": {"targets": ""},
        },
        "port_monitor_schedule": {
            "task": "workers.port_monitor.worker",
            "schedule": crontab(hour=1, minute=0),
            "kwargs": {"targets": "", "options": "-n -Pn -sT -p1-65535"},
        },
        "awvs_do_scan_schedule": {
            "task": "workers.amqp.worker",
            "schedule": crontab(hour=4, minute=0),
            "kwargs": {"task": "awvs", "targets": "", "options": "do scan"},
        },
        "awvs_get_report_schedule": {
            "task": "workers.amqp.worker",
            "schedule": crontab(hour=7, minute=0),
            "kwargs": {"task": "awvs", "targets": "127.0.0.1:8088", "options": "get report"},
        },
        "nessus_do_scan_schedule": {
            "task": "workers.amqp.worker",
            "schedule": crontab(hour=0, minute=0),
            "kwargs": {"task": "nessus", "targets": "", "options": "do scan"},
        },
        "nessus_get_report_schedule": {
            "task": "workers.amqp.worker",
            "schedule": crontab(hour=3, minute=0),
            "kwargs": {"task": "nessus", "targets": "", "options": "do scan"},
        },
    }

    @staticmethod
    def init_app(app):
        pass


config = Config
