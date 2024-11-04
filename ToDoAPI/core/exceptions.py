from rest_framework import status
from rest_framework.exceptions import APIException


class GeneralException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    code = 1000
    summary = "Error"
    verbose = False
    error_detail = None

    def __init__(self, message=None, status_code=None, error_detail=None):
        if not message:
            message = "Oops! Something went wrong, please try again"
        if status_code:
            self.status_code = status_code
        if error_detail:
            message = error_detail
        super().__init__(message)

    def serialize(self):
        data = {
            "code": self.code,
            "summary": self.summary,
            "message": self.detail,
        }
        return data


class InvalidDataException(GeneralException):
    code = 1001
    verbose = True

    def __init__(self, message=None, field=None, status_code=None, error_detail=None):
        if field:
            message = f"Input {field} error."
        super().__init__(message, status_code)


class ParseJsonErrorException(GeneralException):
    code = 1002
    verbose = True

    def __init__(self, message=None):
        if not message:
            message = "Json parse error."
        super().__init__(message=message)


class UnauthorizedException(GeneralException):
    code = 1003
    verbose = True

    def __init__(self, message=None, status_code=status.HTTP_401_UNAUTHORIZED):
        if not message:
            message = "You need to login into the system to use this function."
        super().__init__(message=message)
