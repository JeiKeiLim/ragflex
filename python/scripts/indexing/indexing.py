""" Indexing manager module.

 - Author: Jongkuk Lim
 - Contact: lim.jeikei@gmail.com
"""

import numpy as np

from omegaconf import DictConfig
from typing import Any
from abc import ABC, abstractmethod


class IndexingManager(ABC):
    """Indexing manager class.

    This abstract class is responsible for managing the indexing for the embeddings.
    """

    def __init__(self, embeddings: np.ndarray):
        """Initialize the indexing manager.

        Args:
            embeddings: The embeddings to index.
        """
        self._embeddings = embeddings
        self._index = self._create_index()

    @abstractmethod
    def _create_index(self) -> Any:
        """Create the index.

        Returns:
            The index.
        """
        pass

    @abstractmethod
    def query(self, query: np.ndarray, **kwargs) -> np.ndarray:
        """Query the index.

        Args:
            query: The query.
            k: The number of results to return.

        Returns:
            The results.
        """
        pass


def indexing_manager_factory(
    config: DictConfig, embeddings: np.ndarray
) -> IndexingManager:
    """Create an indexing manager for the given embeddings.

    Args:
        embeddings: The embeddings to create the indexing manager for.

    Returns:
        The indexing manager.
    """
    try:
        return getattr(
            __import__("scripts.indexing", fromlist=[""]), config.class_name
        )(embeddings=embeddings, **config.params)
    except AttributeError:
        raise ValueError(f"Invalid embedding manager class: {config.class_name}")
