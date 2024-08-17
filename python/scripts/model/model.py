"""Model manager module.

 - Author: Jongkuk Lim
 - Contact: lim.jeikei@gmail.com
"""

from abc import ABC, abstractmethod
from omegaconf import DictConfig


class ModelManager(ABC):
    """Model manager class.

    This abstract class is responsible for managing the model.
    """

    def query(self, context: str, query: str, **kwargs) -> str:
        """Query the model.

        Args:
            context: The context.
            query: The query.

        Returns:
            The response.
        """
        return self._query(context, query, **kwargs)

    @abstractmethod
    def _query(self, context: str, query: str, **kwargs) -> str:
        """Query the model.

        Args:
            query: The query.

        Returns:
            The response.
        """
        pass


def model_manager_factory(
    config: DictConfig
) -> ModelManager:
    """Create an model manager

    Args:
        config: Hydra configuration

    Returns:
        The model manager.
    """
    try:
        return getattr(
            __import__("scripts.model", fromlist=[""]), config.class_name
        )(**config.params)
    except AttributeError:
        raise ValueError(f"Invalid embedding manager class: {config.class_name}")
