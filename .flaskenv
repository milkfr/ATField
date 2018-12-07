FLASK_APP=wsgi.py
FLASK_ENV=development
FLASK_SECRET_KEY=123
FLASK_DATABASE_URI=mysql+pymysql://mysql:mysql@mysql/atfield
FLASK_CELERY_BROKER_URL='amqp://rabbitmq:rabbitmq@rabbitmq:5672/atfield'
