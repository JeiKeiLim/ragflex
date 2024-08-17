from scripts.content_extractor.pdf_extractor import PDFExtractor
from scripts.embedding.embedding import ContextManager, get_embeddings
from scripts.indexing import FaissIndexer
from scripts.openai_query import OpenAIQuery

from fastapi import File, UploadFile, APIRouter
from openai import OpenAI

import os

from typing import Dict, Optional


class FastAPIApp:
    UPLOAD_FILE_ROOT = "uploaded_files"

    def __init__(self):
        self._router = APIRouter()
        self._router.add_api_route(
            "/uploadfile", self.upload_file, methods=["POST", "OPTIONS"]
        )
        self._router.add_api_route("/query", self.query, methods=["POST", "OPTIONS"])

        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise ValueError("OPENAI_API_KEY not set")

        self._openai_client = OpenAI(api_key=openai_key)

        self._context_manager: Optional[ContextManager] = None
        self._index_manager: Optional[FaissIndexer] = None
        self._openai_query = OpenAIQuery(self._openai_client)

    @property
    def router(self):
        return self._router

    async def upload_file(self, file: UploadFile = File(...)) -> Dict:
        """Upload a file and process it"""
        content = await file.read()
        pdf_processor = PDFExtractor(content)
        self._context_manager = ContextManager(
            self._openai_client, pdf_processor.content
        )
        self._index_manager = FaissIndexer(self._context_manager.embeddings)

        return {"state": "success!", "filename": file.filename}

    async def query(self, query_data: Dict):
        query = query_data.get("query")
        if not self._context_manager:
            return {"response": "No file uploaded"}

        context_k = query_data.get("context", {}).get("k", 10)
        context_dist_threshold = query_data.get("context", {}).get(
            "distance_threshold", 0.5
        )

        query_embedding = get_embeddings(self._openai_client, query)
        index = self._index_manager.search(
            query_embedding, context_k, context_dist_threshold
        )
        context = self._context_manager.text_at(index)

        context += "\n" + self._openai_query.query(
            context,
            "Summarize the context. Your response must match the language of the context. Do not miss any information.",
        )

        response = self._openai_query.query(context, query)

        return {"query": query, "context": context, "response": response}
