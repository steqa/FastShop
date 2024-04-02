from fastapi import status
from fastapi.exceptions import HTTPException, RequestValidationError


# ----------------------------- Validation Errors -----------------------------

class BaseValidationError(RequestValidationError):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    field = message = type = 'string'

    def __init__(self):
        super().__init__(self.errors())

    @classmethod
    def errors(cls) -> dict:
        return {
            'loc': ['body', cls.field],
            'msg': cls.message,
            'type': cls.type
        }


class MultiValidationError(RequestValidationError):
    def __init__(self, error_classes, status_code: int):
        self.status_code = status_code
        errors = [error.errors() for error in error_classes]
        super().__init__(errors)


class UserEmailExists(BaseValidationError):
    status_code = status.HTTP_409_CONFLICT
    field = 'email'
    message = 'Email already registered'
    type = 'value_error'


class UserPhoneNumberExists(BaseValidationError):
    status_code = status.HTTP_409_CONFLICT
    field = 'phone_number'
    message = 'Phone number already registered'
    type = 'value_error'


# ------------------------------ HTTP Exceptions ------------------------------

class BaseHTTPException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Bad Request'

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail
        )


class UserNotFound(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'User not found'
