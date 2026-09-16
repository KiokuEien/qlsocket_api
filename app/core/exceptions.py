class AppError(Exception):
    status_code = 400
    code = 'BAD_REQUEST'
    message = 'Invalid request data'

    def __init__(self, message: str | None = None):
        self.message = message or self.__class__.__name__

class NotFoundError(AppError):
    status_code = 404
    code = 'NOT_FOUND'
    message = 'Resource nof found'

class ForbiddenError(AppError):
    status_code = 403
    code = 'FORBIDDEN'
    message = 'Access denied'


class ConflictError(AppError):
    status_code = 409
    code = 'CONFLICT'
    message = 'Operation violates data constraints'

class DuplicateError(ConflictError):
    code = 'DUPLICATE'
    message = 'Resource already exists'

class ForeignKeyError(ConflictError):
    code = 'FOREIGN_KEY'
    message = 'Referenced resource does not exists'
