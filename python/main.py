from scripts.pdf_processor import PDFProcessor
from scripts.embedding import get_embeddings, ContextManager
from scripts.indexing import FaissIndexer
from scripts.openai_query import OpenAIQuery

import openai
import os

if __name__ == "__main__":
    # Retrieve the OPENAPI_KEY from the system environment
    openapi_key = os.getenv("OPENAI_API_KEY")
    if openapi_key is None:
        print("OPENAI_API_KEY is not set")
        exit(1)

    client = openai.OpenAI(api_key=openapi_key)

    pdf_path = "res/2023_연말정산.pdf"

    pdf_processor = PDFProcessor(pdf_path)
    context_manager = ContextManager(client, pdf_processor.pdf_text)
    openai_query = OpenAIQuery(client)
    faiss_indexer = FaissIndexer(context_manager.embeddings)

    query = "연말정산 어떻게 진행되는지 알려줘"
    query_embedding = get_embeddings(client, query)

    index = faiss_indexer.search(query_embedding, 10)

    context = context_manager.text_at(index)

    response = openai_query.query(context, query)

    print(response)
