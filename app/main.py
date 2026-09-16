from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from app.core.handlers import register_exception_handler
from app.core.config import settings

from app.api.v1.routes.category import router as category_router

app = FastAPI()

app.include_router(category_router, prefix=settings.api_v1_prefix, tags=['Category'])
register_exception_handler(app)

@app.get('/')
async def root():
    return JSONResponse(
        content={
            'message': 'Hello World!',
            'status': status.HTTP_200_OK,
        },
    )