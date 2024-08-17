"""FastAPI application for the LLM RAG engine.

 - Author: Jongkuk Lim
 - Contact: lim.jeikei@gmail.com
"""

from scripts.content_extractor.pdf_extractor import PDFExtractor
from scripts.embedding.embedding import EmbeddingManager, embedding_manager_factory
from scripts.indexing import FaissIndexer, indexing_manager_factory
from scripts.model import ModelManager, model_manager_factory

from fastapi import File, UploadFile, APIRouter
from openai import OpenAI
from omegaconf import DictConfig


import os

from typing import Dict, Optional


class FastAPIApp:
    UPLOAD_FILE_ROOT = "uploaded_files"

    def __init__(self, config: DictConfig):
        self._config = config
        self._router = APIRouter()
        self._router.add_api_route(
            "/uploadfile", self.upload_file, methods=["POST", "OPTIONS"]
        )
        self._router.add_api_route("/query", self.query, methods=["POST", "OPTIONS"])

        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY not set")

        self._openai_client = OpenAI(api_key=openai_key)

        self._embedding_manager: Optional[EmbeddingManager] = None
        self._index_manager: Optional[FaissIndexer] = None
        self._llm_model: ModelManager = model_manager_factory(self._config.model)

    @property
    def router(self):
        return self._router

    async def upload_file(self, file: UploadFile = File(...)) -> Dict:
        """Upload a file and process it"""
        content = await file.read()
        pdf_processor = PDFExtractor(content)

        if self._embedding_manager is None:
            self._embedding_manager = embedding_manager_factory(
                self._config.embedding, pdf_processor.content
            )

        self._index_manager = indexing_manager_factory(
            self._config.indexing, self._embedding_manager.embeddings
        )

        return {"state": "success!", "filename": file.filename}

    async def query(self, query_data: Dict):
        """Query LLM result for the given query.

        Body should be a JSON object with the following fields:
        - query: The query to search for.
        - params: The parameters for the query (optional).
        """
        query = query_data.get("query")
        if not self._embedding_manager:
            return {"response": "No file uploaded"}

        query_params = query_data.get("params", {})

        query_embedding = self._embedding_manager.generate_embeddings(query)

        index = self._index_manager.query(query_embedding, **query_params)
        context = self._embedding_manager.text_at(index)

        context += "\n" + self._llm_model.query(
            context,
            "Summarize the context. Your response must match the language of the context. Do not miss any information.",
        )

        response = self._llm_model.query(context, query)

        return {"query": query, "context": context, "response": response}
