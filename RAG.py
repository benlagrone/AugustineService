# RAG.py
from llama_index.core import SimpleDirectoryReader, GPTVectorStoreIndex
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.settings import Settings
Settings.llm = None

# Use a specific embedding model
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

def initialize_index():
    """
    Initialize or load the index with Augustine's texts.
    """
    try:
        # Try to load the pre-built index
        storage_context = StorageContext.from_defaults(persist_dir="./augustine_index")
        index = load_index_from_storage(storage_context, embed_model=embed_model)
        print("Loaded existing index from storage")
    except Exception:
        print("Building new index...")
        # Load Augustine's texts
        documents = SimpleDirectoryReader("./augustine_texts").load_data()
        # Create new index
        index = GPTVectorStoreIndex.from_documents(
            documents,
            embed_model=embed_model
        )
        # Save the index
        index.storage_context.persist(persist_dir="./augustine_index")
        print("New index built and saved")
    return index

# Initialize the index and query engine
index = initialize_index()
query_engine = index.as_query_engine(
    response_mode="tree_summarize",
    similarity_top_k=3,
    llm=None
)

def get_context(query, author="Augustine"):
    """
    Retrieve relevant context for a given query.
    """
    try:
        response = query_engine.query(query)
        context = str(response)
        if not context.strip():
            return "I apologize, but I couldn't find relevant passages for this query."
        return context
    except Exception as e:
        print(f"Error in get_context: {str(e)}")
        return "I apologize, but there was an error retrieving the context."

# Example usage (can be commented out in production)
if __name__ == "__main__":
    test_query = "What does Augustine say about grace?"
    response = get_context(test_query)
    print("\nTest Query:", test_query)
    print("\nResponse:", response)