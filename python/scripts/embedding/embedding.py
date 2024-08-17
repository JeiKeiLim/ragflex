import openai
import numpy as np
import hashlib
import tempfile
import os

from typing import List, Union


class ContextManager:
    CACHE_ROOT = tempfile.gettempdir()

    def __init__(self, client: openai.OpenAI, text: str):
        self._client = client
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

        embeddings = get_embeddings(self._client, self._split_text)
        np.save(cache_path, embeddings)

        return embeddings

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


def get_embeddings(client: openai.OpenAI, text: Union[str, List[str]]) -> np.ndarray:
    """Get the embeddings for the text.

    Args:
        client: The OpenAI client.
        text: The text to get the embeddings for.

    Returns:
        The embeddings for the text.
    """
    input_text = [text] if isinstance(text, str) else text
    embeddings = []

    if len(input_text) < 1024:
        input_texts = [input_text]
    else:
        input_texts = [
            input_text[i : i + 1024] for i in range(0, len(input_text), 1024)
        ]

    for input_text in input_texts:
        response = client.embeddings.create(
            input=input_text, model="text-embedding-ada-002"
        )
        embeddings += [res.embedding for res in response.data]

    return np.array(embeddings)
