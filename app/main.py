from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from app.core.handlers import register_exception_handler


app = FastAPI()

register_exception_handler(app)

@app.get('/')
async def root():
    return JSONResponse(
        content={
            'message': 'Hello World!',
            'status': status.HTTP_200_OK,
        },
    )