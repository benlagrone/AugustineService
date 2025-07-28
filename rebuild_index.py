# rebuild_index.py
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def rebuild_index():
    print("Loading embedding model...")
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    print("Loading documents...")
    documents = SimpleDirectoryReader("./augustine_texts").load_data()
    
    print("Creating index...")
    index = VectorStoreIndex.from_documents(
        documents,
        embed_model=embed_model
    )
    
    print("Saving index...")
    index.storage_context.persist(persist_dir="./augustine_index")
    
    print("Index rebuilt successfully!")

if __name__ == "__main__":
    rebuild_index()