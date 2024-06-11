import faiss
import numpy as np

class FaissIndexer:
    def __init__(self, embeddings: np.ndarray):
        self._embeddings = embeddings
        self._faiss_index = faiss.IndexFlatL2(self._embeddings.shape[1])
        self._faiss_index.add(self._embeddings)

    def search(self,
                query_embedding: np.ndarray,
                k: int,
                distance_threshold: float = 0.5) -> np.ndarray:
        distance, index = self._faiss_index.search(query_embedding, k)
        return index[0][distance[0] < distance_threshold]