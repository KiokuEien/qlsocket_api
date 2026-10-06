from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import AppError



def register_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        orig = exc.orig
        error_message = {
            'code': 'CONFLICT_ERROR',
            'type': 'db_error',
            'message': getattr(orig.__cause__, 'detail', 'Operation violates data constraints')
        }

        match orig.sqlstate:
            case '23505':
                error_message['code'] = 'DUPLICATE_ERROR'
            case '23503':
                error_message['code'] = 'FOREIGN_KEY_ERROR'
            case '23502':
                error_message['code'] = 'NOT_NULL_ERROR'


        return JSONResponse(
            status_code=409,
            content={
                'success': False,
                'error': error_message,
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        error = exc.errors()[0]
        error_message = {
            'code': 'VALIDATION_ERROR',
            'type': error['type'],
            'field': '.'.join(str(x) for x in error['loc'] if x != 'body'),
            'message': error.get('msg', 'Invalid request'),
        }

        if error['type'] == 'json_invalid':
            error_message = {
                'code': 'JSON_DECODE_ERROR',
                'type': 'json_invalid',
                'message': error['ctx']['error'],
            }

        return JSONResponse(
            status_code=422,
            content={
                'success': False,
                'error': error_message,
            }
        )

    @app.exception_handler(AppError)
    async def app_exception_handler(request: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                'success': False,
                'error': {
                    'code': exc.code,
                    'message': exc.message
                }
            }
        )


    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                'success': False,
                'error': {
                    'code': 'INTERNAL_SERVER_ERROR',
                    'message': 'Internal server error'
                }
            }
        )