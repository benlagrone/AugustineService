from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import os

# Load a local embedding model
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Directory containing Augustine's works
TEXTS_DIR = "./augustine_texts/"

# Load documents with verbose output
print(f"Loading documents from {TEXTS_DIR}")
documents = SimpleDirectoryReader(TEXTS_DIR).load_data()
print(f"Loaded {len(documents)} documents")

# Create an index using local embeddings
print("Creating index...")
index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

# Persist the index
print("Saving index...")
index.storage_context.persist(persist_dir="./augustine_index")

print("Indexed Augustine's works successfully with local embeddings!")