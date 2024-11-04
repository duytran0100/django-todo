from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, ParseError, ValidationError
from rest_framework.response import Response
from rest_framework.views import exception_handler

from core.exceptions import (
    GeneralException,
    UnauthorizedException,
    ParseJsonErrorException,
    InvalidDataException,
)
from core.utils import get_logger

logger = get_logger(__name__)


def response_error(ex, status_code=status.HTTP_400_BAD_REQUEST):
    if not isinstance(ex, GeneralException):
        if (
            isinstance(ex, DjangoValidationError)
            and hasattr(ex, "code")
            and ex.code == "invalid"
        ):
            ex = InvalidDataException(message=ex.message[0], status_code=400)
            return Response(
                data=ex.serialize(), status_code=status.HTTP_400_BAD_REQUEST
            )
        ex = GeneralException(message=str(ex), status_code=status_code)

    error_message = "Oops! Something went wrong, please try again."
    if ex.verbose is True:
        error_message = str(ex)

    error = {"code": ex.code, "message": error_message, "summary": ex.summary}
    return Response(data=error, status=ex.status_code)


def parse_validation_error(exc: Exception) -> GeneralException:
    if isinstance(exc, NotAuthenticated):
        return UnauthorizedException()

    if isinstance(exc, ValidationError):
        field = list(exc.detail.keys())[0]
        error_detail = str(exc.detail.get(field)[0])
        return InvalidDataException(field=field, error_detail=error_detail)

    if isinstance(exc, ParseError):
        return ParseJsonErrorException(message=str(exc.detail))

    if isinstance(exc, GeneralException):
        return exc

    return GeneralException(str(exc))


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    logger.exception(exc)

    response = exception_handler(exc, context)
    # Handle Error of 500
    if not response:
        return response_error(exc)

    # Parse Generic Exception
    ex = parse_validation_error(exc)
    response.data = ex.serialize()
    return response
