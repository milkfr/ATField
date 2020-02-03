from app import celery, create_app
from elasticsearch6 import Elasticsearch

app = create_app()

es = Elasticsearch(
    [app.config.get('ES_HOST')],
    http_auth=(app.config.get('ES_USERNAME'), app.config.get('ES_PASSWORD')),
    port=app.config.get('ES_PORT'),
)

app.app_context().push()
