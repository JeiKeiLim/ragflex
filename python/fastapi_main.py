"""Main FastAPI application entry point.

 - Author: Jongkuk Lim
 - Contact: lim.jeikei@gmail.com
"""

import hydra
import uvicorn
import tempfile
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from omegaconf import DictConfig, OmegaConf

from scripts.fastapi_app import FastAPIApp


def save_hydra_config_to_tempfile(config: DictConfig):
    temp_file_path = os.path.join(tempfile.gettempdir(), "ragflex_config.yaml")
    print(temp_file_path)
    OmegaConf.save(config, temp_file_path)


def load_temp_hydra_config() -> DictConfig:
    temp_file_path = os.path.join(tempfile.gettempdir(), "ragflex_config.yaml")
    return OmegaConf.load(temp_file_path)


def create_app() -> FastAPI:
    config = load_temp_hydra_config()

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fastapi_app = FastAPIApp(config)
    app.include_router(fastapi_app.router)
    return app


app = create_app()


@hydra.main(version_base=None, config_path="config", config_name="base_config")
def main_app(config: DictConfig):
    save_hydra_config_to_tempfile(config)

    uvicorn.run(
        "fastapi_main:app", host=config.app.host, port=config.app.port, reload=True
    )


if __name__ == "__main__":
    main_app()
