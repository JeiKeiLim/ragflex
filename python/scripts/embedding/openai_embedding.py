"""OpenAI embedding module.

 - Author: Jongkuk Lim
 - Contact: lim.jeikei@gmail.com
"""

import numpy as np
import os

from typing import List
from openai import OpenAI

from scripts.embedding.embedding import EmbeddingManager


class OpenAIEmbedding(EmbeddingManager):
    """OpenAI embedding class.

    This class is responsible for getting the embeddings from the OpenAI API.
    """

    def __init__(
        self, text: str, max_batch_size=1024, embedding_model="text-embedding-ada-002"
    ):
        """Initialize the OpenAI embedding.

        Args:
            client: The OpenAI client.
            text: The text to get the embeddings for.
        """
        self.__max_batch_size = max_batch_size
        self.__embedding_model = embedding_model

        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY not set")

        self._client = OpenAI(api_key=openai_key)
        super().__init__(text)


    def _generate_embeddings(self, split_texts: List[str]) -> np.ndarray:
        """Get the embeddings of texts list.

        Returns:
            The embeddings for each text.
        """
        embeddings = []

        if len(split_texts) < self.__max_batch_size:
            input_texts = [split_texts]
        else:
            input_texts = [
                split_texts[i : i + self.__max_batch_size]
                for i in range(0, len(split_texts), self.__max_batch_size)
            ]

        for input_text in input_texts:
            response = self._client.embeddings.create(
                input=input_text, model=self.__embedding_model
            )
            embeddings += [res.embedding for res in response.data]

        return np.array(embeddings)
