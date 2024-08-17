# RAGFlex

RAGFlex is a flexible Retrieval Augmented Generation (RAG) framework that allows you to configure pipeline with [https://hydra.cc/](hydra) configuration files with [https://fastapi.tiangolo.com/](FastAPI) as the backend and [https://flutter.dev/](flutter) as the frontend.


# Getting started
## Setup with conda
```bash
# Create a new conda environment
conda env create -f environment.yml

# Activate the environment
conda activate ragflex
```

## Start the backend
```bash
cd python

# If you are using the default openai api configuration
OPENAI_API_KEY=$OPENAI_API_KEY python fastapi_main.py
```

## Start the frontend

```bash
cd flutter

# Run as a web server
flutter run -d web-server --web-hostname=0.0.0.0
```
