from scripts.fastapi_app import FastAPIApp
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

app = FastAPI()
fastapi_app = FastAPIApp()
app.include_router(fastapi_app.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)