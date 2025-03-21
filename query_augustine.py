from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding  # Local embeddings
from llama_index.llms.ollama import Ollama  # Use Ollama as the LLM
from llama_index.core.query_engine import RetrieverQueryEngine
import ollama

# Load local embedding model
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load stored index with the correct embedding model
storage_context = StorageContext.from_defaults(persist_dir="./augustine_index")
index = load_index_from_storage(storage_context, embed_model=embed_model)

# Set Ollama as the default LLM
# llm = Ollama(model="mistral")  # Change to "augustine" if you fine-tuned it
llm = Ollama(model="augustine")

# Create a query engine using Ollama and the indexed texts
query_engine = RetrieverQueryEngine.from_args(index.as_retriever(), llm=llm)


# Function to query the RAG system
def query_augustine(question):
    """Queries the Augustine RAG index and returns a properly formatted response."""

    # Retrieve relevant passages
    response = query_engine.query(question)
    
    # Convert response to string and clean up phrasing
    formatted_response = str(response)
    
    # Remove disclaimers and qualifiers
    remove_phrases = [
        "While it is not possible to have Augustine directly",
        "Augustine might say",
        "Based on Augustine's writings",
        "It is likely that Augustine would respond",
        "According to Augustine's thoughts",
        "In his writings, Augustine"
    ]
    
    for phrase in remove_phrases:
        formatted_response = formatted_response.replace(phrase, "")
    
    # Improve readability
    formatted_response = formatted_response.strip()
    
    # Replace with a more personal tone
    formatted_response = formatted_response.replace("I ", "🧙‍♂️ I ").replace("My dear child,", "🧙‍♂️ My dear child,")
    
    return formatted_response

# Test Query
question = "Have Augustine say a prayer for my job hunt?"
response = query_augustine(question)

print("\n Augustine's Response:\n")
print(response)