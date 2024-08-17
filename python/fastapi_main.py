import hydra
import uvicorn
import tempfile
import os

from omegaconf import DictConfig, OmegaConf


def save_hydra_config_to_tempfile(config: DictConfig):
    temp_file_path = os.path.join(tempfile.gettempdir(), "ragflex_config.yaml")
    print(temp_file_path)
    OmegaConf.save(config, temp_file_path)


@hydra.main(version_base=None, config_path="config", config_name="base_config")
def main_app(config: DictConfig):
    print(config)

    save_hydra_config_to_tempfile(config)

    uvicorn.run(
        "fastapi_app:app", host=config.app.host, port=config.app.port, reload=True
    )


if __name__ == "__main__":
    main_app()
