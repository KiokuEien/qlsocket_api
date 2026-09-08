from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get('/')
async def root():
    return JSONResponse(
        content={
            'message': 'Hello World!',
            'status': status.HTTP_200_OK,
        },
    )