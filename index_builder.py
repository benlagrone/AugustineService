# index_builder.py
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core import SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def build_index():
    print("Loading documents...")
    documents = SimpleDirectoryReader("./augustine_texts").load_data()
    
    print("Creating index...")
    index = VectorStoreIndex.from_documents(documents)
    
    print("Saving index...")
    index.storage_context.persist(persist_dir="./augustine_index")
    
    print("Index built and saved!")

if __name__ == "__main__":
    build_index()