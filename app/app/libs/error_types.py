from app.libs.errors import APIException


class ServerException(APIException):
    code = 500
    msg = ('server exception',)
    error_code = 1000


class BadRequestException(APIException):
    code = 400
    msg = (
        'bad request exception',
        'request cannot be understood or parameter error'
    )
    error_code = 1001


class ParamException(BadRequestException):
    msg = (
        'bad request exception',
        'invalid parameter'
    )
    error_code = 1002


class PrivilegeException(APIException):
    code = 403
    msg = (
        'privilege exception',
        'insufficient privilege'
    )
    error_code = 1003


class NotFoundException(APIException):
    code = 404
    msg = (
        'not found exception',
        'the requested resource was not found'
    )
    error_code = 1004


class AuthFailedException(APIException):
    code = 401
    msg = ('authorization failed exception',)
    error_code = 1005
