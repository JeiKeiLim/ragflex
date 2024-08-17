"""Example of main script to run the pipeline without FastAPI.

 - Author: Jongkuk Lim
 - Contact: lim.jeikei@gmail.com
"""

import hydra

from omegaconf import DictConfig

from scripts.content_extractor.pdf_extractor import PDFExtractor
from scripts.embedding import embedding_manager_factory
from scripts.indexing import indexing_manager_factory
from scripts.model import model_manager_factory


@hydra.main(version_base=None, config_path="config", config_name="base_config")
def main(config: DictConfig):
    print(config)

    pdf_path = "res/2023_연말정산.pdf"
    pdf_processor = PDFExtractor(pdf_path)

    embedding_manager = embedding_manager_factory(
        config.embedding, pdf_processor.content
    )
    indexing_manager = indexing_manager_factory(
        config.indexing, embedding_manager.embeddings
    )
    model_manager = model_manager_factory(config.model)

    query = "연말정산 어떻게 진행되는지 알려줘"
    query_embedding = embedding_manager.generate_embeddings(query)

    index = indexing_manager.query(query_embedding)
    context = embedding_manager.text_at(index)

    response = model_manager.query(context, query)

    print(response)


if __name__ == "__main__":
    main()
