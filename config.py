"""
Configuration file for the Job Search AI application
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Vector Store Configuration
VECTOR_STORE_PATH = "context/vectorstore"
UPLOAD_DIR = "context/uploads"
PROMPT_DIR = "context/prompts"

# Chunk Configuration for document processing
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Model Configuration
DEFAULT_MODEL = "gpt-4.1"
EMBEDDING_MODEL = "text-embedding-ada-002"

# Personal Context Configuration
CONTEXT_FILE_PATH = "context/background/personal_context.txt"

# Ensure directories exist
os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)