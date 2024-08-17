"""Embedding manager module.

 - Author: Jongkuk Lim
 - Contact: lim.jeikei@gmail.com
"""

import numpy as np
import hashlib
import tempfile
import os

from abc import ABC, abstractmethod
from omegaconf import DictConfig

from typing import List, Union


class EmbeddingManager(ABC):
    """Embedding manager class.

    This abstract class is responsible for managing the embeddings for the text.
    """

    CACHE_ROOT = tempfile.gettempdir()

    def __init__(self, text: str):
        """Initialize the embedding manager.

        Args:
            client: The OpenAI client.
            text: The text to get the embeddings for.
        """
        self._text = text
        self._text_hash = hashlib.sha256(text.encode()).hexdigest()
        self._split_text = self._split_text_into_lines(text)
        self._embeddings = self._get_embeddings()

    def _split_text_into_lines(self, text: str) -> List[str]:
        """Split the text into lines.

        This is useful for splitting the text into lines when we want to get the embeddings for each line.
        @TODO: This should be done in a more efficient way.

        Args:
            text: The text to split into arrays.

        Returns:
            The lines of the text.
        """
        return [line for line in text.split("\n") if line != ""]

    def _get_embeddings(self) -> np.ndarray:
        """Get the embeddings for the text.

        Embeddings are cached to disk.
        """
        cache_path = os.path.join(self.CACHE_ROOT, f"{self._text_hash}.npy")

        if os.path.exists(cache_path):
            print(f"Loading embeddings from {cache_path}")
            return np.load(cache_path)

        embeddings = self._generate_embeddings(self._split_text)
        np.save(cache_path, embeddings)

        return embeddings

    def generate_embeddings(self, split_texts: Union[List[str], str]) -> np.ndarray:
        """Get the embeddings of texts list.

        ex) split_texts = ["Hello, world!", "How are you?"]
            return np.array([[0.1, 0.2, ...], [0.3, 0.4, ...]])

        Returns:
            The embeddings for each text.
        """
        if isinstance(split_texts, str):
            input_texts = [split_texts]
        else:
            input_texts = split_texts

        return self._generate_embeddings(input_texts)

    @abstractmethod
    def _generate_embeddings(self, split_texts: List[str]) -> np.ndarray:
        """Get the embeddings of texts list.

        Returns:
            The embeddings for each text.
        """
        pass

    def text_at(self, index: Union[int, List[int]]) -> str:
        """Get the text at the given index.

        Args:
            index: The index of the text to get.

        Returns:
            The text at the given index.
        """
        # TODO: Perhaps we should pass this text to OpenAI to extract useful information.
        if isinstance(index, int):
            return self._split_text[index]
        else:
            return "\n".join([self._split_text[i] for i in index])

    @property
    def embeddings(self) -> np.ndarray:
        return self._embeddings

    @property
    def text(self) -> str:
        return self._text


def embedding_manager_factory(config: DictConfig, text: str) -> EmbeddingManager:
    """Create an embedding manager for the given text.

    Args:
        text: The text to create the embedding manager for.

    Returns:
        The embedding manager.
    """
    try:
        return getattr(
            __import__("scripts.embedding", fromlist=[""]),
            config.class_name
        )(text=text, **config.params)
    except AttributeError:
        raise ValueError(f"Invalid embedding manager class: {config.class_name}")
