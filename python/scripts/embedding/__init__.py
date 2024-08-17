""" This module is responsible for managing the embeddings.

 - Author: Jongkuk Lim
 - Contact: lim.jeikei@gmail.com
"""

from scripts.embedding.embedding import EmbeddingManager, embedding_manager_factory
from scripts.embedding.openai_embedding import OpenAIEmbedding

__all__ = [
    "EmbeddingManager",
    "OpenAIEmbedding",
    "embedding_manager_factory",
]
