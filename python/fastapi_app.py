import tempfile
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from omegaconf import DictConfig, OmegaConf

from scripts.fastapi_app import FastAPIApp


def load_temp_hydra_config() -> DictConfig:
    temp_file_path = os.path.join(tempfile.gettempdir(), "ragflex_config.yaml")
    return OmegaConf.load(temp_file_path)


def create_app() -> FastAPI:
    config = load_temp_hydra_config()
    print("Config from create_app:", config)
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fastapi_app = FastAPIApp()
    app.include_router(fastapi_app.router)
    return app


app = create_app()
