from sqlalchemy.exc import IntegrityError

from app.core.exceptions import DuplicateError, ForeignKeyError, ConflictError

def map_integrity_error(exc: IntegrityError) -> DuplicateError | ForeignKeyError | ConflictError:
    exc_code = getattr(exc.orig, 'pgcode', None)

    if exc_code == '23505':
        return DuplicateError()
    if exc_code == '23503':
        return ForeignKeyError()

    return ConflictError()