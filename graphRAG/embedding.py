from sentence_transformers import SentenceTransformer
from config import OPENAI_MODEL

class GraphRAGEmbedder:
    """Wrapper class to provide an 'embed_query' method for GraphRAG."""
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_query(self, text):
        """Wraps the model encode function to match expected API."""
        return self.model.encode(text, convert_to_tensor=True).tolist()

def load_embedder():
    """Loads SentenceTransformer and ensures compatibility with GraphRAG."""
    print(f"DEBUG: Loading embedding model: sentence-transformers/all-MiniLM-L6-v2")
    return GraphRAGEmbedder()

