"""This module is responsible for managing the indexing of embeddings.

 - Author: Jongkuk Lim
 - Contact: lim.jeikei@gmail.com
"""

from scripts.indexing.indexing import IndexingManager, indexing_manager_factory
from scripts.indexing.faiss_indexing import FaissIndexer

__all__ = [
    "IndexingManager",
    "FaissIndexer",
    "indexing_manager_factory",
]
