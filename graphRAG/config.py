import os
from dotenv import load_dotenv

load_dotenv()

VECTOR_INDEX_NAME = "group_vector_index"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"

if not OPENAI_API_KEY:
    raise ValueError("ERROR: OPENAI_API_KEY is not set in .env file")