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

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("FLASK_DATABASE_URI",
                                             "sqlite:///"+os.path.join(basedir, "data-dev.sqlite"))
    ELASTICSEARCH_HOST = os.environ.get("FLASK_ELASTICSEARCH_HOST", "localhost:9200")
    CELERY_RESULT_BACKEND = os.environ.get("FLASK_CELERY_RESULT_BACKEND")
    CELERY_BROKER_URL = os.environ.get("FLASK_CELERY_BROKER_URL")
    CELERY_QUEUES = (
        Queue("default", Exchange("default"), routing_key="default"),
        Queue("task_domain_resolution", Exchange("task_domain_resolution"),
              routing_key="task_domain_resolution"),
        Queue("task_service_probe_by_masscan", Exchange("task_service_probe_by_masscan"),
              routing_key="task_service_probe_by_masscan"),
        Queue("task_service_probe_by_nmap", Exchange("task_service_probe_by_nmap"),
              routing_key="task_service_probe_by_nmap")
    )
    # 路由
    CELERY_ROUTES = {
        "app.async.domain_resolution.do_async_scan": {"queue": "task_domain_resolution",
                                                      "routing_key": "task_domain_resolution"},
        "app.async.service_probe_by_masscan.do_async_scan": {"queue": "task_service_probe_by_masscan",
                                                             "routing_key": "task_service_probe_by_masscan"},
        "app.async.service_probe_by_nmap.do_async_scan": {"queue": "task_service_probe_by_nmap",
                                                          "routing_key": "task_service_probe_by_nmap"},
    }

    CELERY_TIMEZONE = "UTC"

    CELERYBEAT_SCHEDULE = {
        "taskA_schedule": {
            "task": "app.async.scan.do_scan_task",
            "schedule": timedelta(seconds=60),
            "args": ("domain resolution",
                     "every day", "none", "www.baidu.com", "test")
        },
        'taskB_scheduler': {
            "task": "app.async.scan.do_scan_task",
            "schedule": timedelta(seconds=60),
            "args": ("service probe by masscan",
                     "every day", "-p1-5000 --rate 1000", "127.0.0.1", "test")
        },
        'add_schedule': {
            "task": "app.async.scan.do_scan_task",
            "schedule": timedelta(seconds=60),
            "args": ("service probe by nmap",
                     "every day", "-n -Pn -sT -p 1-5000", "127.0.0.1", "test")
        }
    }


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("FLASK_DATABASE_URI",
                                             "sqlite:///"+os.path.join(basedir, "data-pro.sqlite"))


config = {
    "default": DevelopmentConfig,
    "production": ProductionConfig,
    "development": DevelopmentConfig,
}
