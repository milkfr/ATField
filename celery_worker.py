import os
from app import celery, create_app
from dotenv import load_dotenv


load_dotenv(dotenv_path=".flaskenv")
app = create_app(os.environ.get("FLASK_CONFIG", default="default"))
print(os.environ.get("FLASK_CONFIG"))
app.app_context().push()
