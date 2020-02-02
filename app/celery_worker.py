from app import celery, create_app
from elasticsearch6 import Elasticsearch


es = Elasticsearch(
    ['localhost'],
    http_auth=('username', 'password'),
    port=9500,
)

app = create_app()
app.app_context().push()
