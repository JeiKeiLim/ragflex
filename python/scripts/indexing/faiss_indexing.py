"""Faiss Indexing Module

 - Author: Jongkuk Lim
 - Contact: lim.jeikei@gmail.com
"""

from typing import Any

import numpy as np

import faiss

from scripts.indexing.indexing import IndexingManager


class FaissIndexer(IndexingManager):
    def __init__(
        self,
        embeddings: np.ndarray,
        index_type: str = "IndexFlatL2",
        distance_threshold: float = 0.5,
        k: int = 10,
    ):
        self._distance_threshold = distance_threshold
        self._k = k

        self.__indexing_type = getattr(faiss, index_type)
        super().__init__(embeddings)

    def _create_index(self) -> Any:
        faiss_index = self.__indexing_type(self._embeddings.shape[1])
        faiss_index.add(self._embeddings)

        return faiss_index

    def query(
        self, query_embedding: np.ndarray, k: int = -1, distance_threshold: float = -1
    ) -> np.ndarray:
        search_k = self._k if k < 0 else k
        search_distance_threshold = (
            self._distance_threshold if distance_threshold < 0 else distance_threshold
        )

        distance, index = self._index.search(query_embedding, search_k)
        return index[0][distance[0] < search_distance_threshold]
