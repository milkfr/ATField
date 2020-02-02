from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
import uuid
from datetime import datetime


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        elif isinstance(o, uuid.UUID):
            return str(o)
        elif isinstance(o, datetime):
            return str(o)
        else:
            super().default(o)
        # raise ServerException()


class Flask(_Flask):
    json_encoder = JSONEncoder
