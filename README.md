# Farmer RAG — AI-Powered Agricultural Assistant

Farmer RAG is a Retrieval-Augmented Generation (RAG) application that helps users access agricultural information from PDF-based agricultural resources. It combines semantic search, vector embeddings, and a large language model to generate context-aware answers in the user's preferred language.

## Overview

Agricultural information is often distributed across government advisories, farming handbooks, and regional agricultural documents. Farmer RAG aims to make this information more accessible through natural-language queries.

The application retrieves relevant information from a ChromaDB vector database and uses a Groq-hosted language model to generate responses grounded in the retrieved context.

## Features

- **PDF-Based Knowledge Retrieval:** Processes agricultural documents using LangChain document loaders.
- **Semantic Search:** Uses Hugging Face sentence embeddings to retrieve relevant information.
- **Retrieval-Augmented Generation:** Combines retrieved document context with an LLM to generate relevant responses.
- **Multilingual Responses:** Allows users to specify their preferred response language.
- **Location Input:** Collects the user's state and city and retrieves geographical coordinates using a geocoding utility.
- **Persistent Vector Database:** Uses ChromaDB to store and retrieve document embeddings.
- **Source Transparency:** Displays the source paths associated with retrieved documents.

## Technology Stack

- **Programming Language:** Python
- **LLM Provider:** Groq API
- **Language Model:** `openai/gpt-oss-20b`
- **LLM Framework:** LangChain
- **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Database:** ChromaDB
- **Document Processing:** PyPDFLoader
- **Text Splitting:** RecursiveCharacterTextSplitter
- **Environment Management:** python-dotenv
- **Geocoding:** Custom Python utility
- **Interface:** Python command-line interface in the current implementation

## Architecture

The application follows a Retrieval-Augmented Generation pipeline:

1. **Document Loading:** Agricultural PDF documents are loaded using PyPDFLoader and DirectoryLoader.
2. **Text Chunking:** Documents are split into smaller chunks using RecursiveCharacterTextSplitter, with a chunk size of 500 characters and an overlap of 80 characters.
3. **Embedding Generation:** Text chunks are converted into vector embeddings using the Hugging Face sentence-transformer model.
4. **Vector Storage:** Embeddings and associated document metadata are stored in ChromaDB.
5. **Semantic Retrieval:** The retriever searches for the eight most relevant chunks for a user's question.
6. **Answer Generation:** The retrieved context is passed to the Groq-hosted LLM, which generates an answer in the requested language.
7. **Source Display:** The application displays the source paths of the retrieved documents.

## Project Structure

```text
farmer-proj/
├── src/
│   ├── main.py
│   ├── farmer_proj/
│   │   └── api/
│   │       └── geocoding.py
│   └── chroma_db/           # Generated locally
├── .env                     # Local API credentials
├── .gitignore
├── pyproject.toml
├── uv.lock                  # If included in the repository
└── README.md
```

The agricultural PDF dataset and generated ChromaDB database are excluded from the GitHub repository. The directory structure above represents the main components and may need to be adjusted to match the actual repository.

## Prerequisites

- Python compatible with the project's dependencies
- A Groq API key
- The `uv` package manager, if using the project's dependency configuration
- Agricultural PDF documents to build the knowledge base
- Internet access for API requests and model downloads

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mohd-umar1/farmer-RAG.git
cd farmer-RAG
```

### 2. Install dependencies

If the project uses `uv`:

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace the placeholder with your own API key. Never commit `.env` or expose API credentials publicly.

### 4. Prepare the agricultural documents

Place your agricultural PDF documents in the local data directory configured in the ingestion code.

The dataset is not included in this repository. You must provide the documents yourself.

### 5. Build the vector database

The PDF ingestion, text-splitting, and database-creation sections in the current `main.py` are commented out. Before running the application for the first time, enable or implement the ingestion pipeline to generate the ChromaDB vector database locally.

The application currently expects an existing vector database and does not automatically rebuild it when the database is missing.

### 6. Run the application

From the project root:

```bash
uv run python src/main.py
```

Follow the prompts to enter your preferred language, state, city, and agricultural question.

Type `exit` to terminate the application.

Adjust the command if your project configuration uses a different entry point.

## Configuration

| Component | Setting |
|---|---|
| LLM provider | Groq |
| Language model | `openai/gpt-oss-20b` |
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` |
| Retrieval count | Top 8 chunks |
| Chunk size | 500 characters |
| Chunk overlap | 80 characters |
| Vector database | ChromaDB |

## Limitations and Future Improvements

- Implement a complete document-ingestion pipeline that creates the vector database automatically.
- Add district-based retrieval filtering using document metadata and location information.
- Evaluate retrieval relevance and answer quality using a curated evaluation dataset.
- Include document page numbers and more precise source citations.
- Improve handling of missing databases, invalid inputs, and API failures.
- Develop a Streamlit interface for a more accessible user experience.
- Benchmark response latency, retrieval quality, and API costs.
- Improve grounding so that document-supported information is clearly distinguished from general agricultural knowledge.

## Security

- Store API keys in environment variables.
- Exclude `.env` from version control.
- Keep local datasets, generated vector databases, and virtual environments out of the repository.
- Never commit API credentials or other sensitive information.

## Author

**Mohd Umar Inamdar**

GitHub: [mohd-umar1](https://github.com/mohd-umar1)

## Disclaimer

Farmer RAG is an educational project exploring the use of retrieval-augmented generation for agricultural information access. Its responses should be verified against reliable agricultural sources before being used to make important farming decisions.
