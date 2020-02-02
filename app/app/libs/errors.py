from flask import json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):

    code = 500
    msg = ('unknown exception',)
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code
        )
        return json.dumps(body)

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]
