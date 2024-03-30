from fastapi.exceptions import RequestValidationError


class MultiValidationError(RequestValidationError):
	def __init__(self, error_classes, status_code: int):
		self.status_code = status_code
		errors = [error.errors() for error in error_classes]
		super().__init__(errors)


class BaseCustomError(Exception):
    @classmethod
    def errors(cls):
        return {
            'loc': ['body', cls.field],
            'msg': cls.message,
            'type': cls.type
        }


class UserEmailExists(BaseCustomError, RequestValidationError):
    field = 'email'
    message = 'Email already registered'
    type = 'value_error'
    
    def __init__(self):
        self.status_code = 409
        super().__init__(self.errors())
        

class UserPhoneNumberExists(BaseCustomError, RequestValidationError):
    field = 'phone_number'
    message = 'Phone number already registered'
    type = 'value_error'
    
    def __init__(self):
        self.status_code = 409
        super().__init__(self.errors())