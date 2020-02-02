from app.libs.errors import APIException


class Success(APIException):
    code = 200
    msg = ''
    error_code = 0


class Created(APIException):
    code = 201
    msg = (
        'created',
    )
    error_code = 0


class NotContent(APIException):
    code = 204
    msg = (
        'not content',
    )
    error_code = 0
