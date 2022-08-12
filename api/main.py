from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from routes import router

tags_metadata = [
    {
        "name": "napa-api",
        "description": "This API is for testing purposes only",
    },
]

app = FastAPI(
    title="NaPA API",
    version="0.0.1",
    docs_url='/api/v1/docs',
    redoc_url='/api/v1/redoc',
    openapi_url='/api/v1/openapi.json',
    openapi_tags=tags_metadata
)

origins = [
    "https://shebogholo.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"],
)

app.include_router(router=router, prefix="/api/v1")
app.mount("/images", StaticFiles(directory="images"), name="images")