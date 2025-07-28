# api/RAG.py
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex

# Load Augustine's texts
documents = SimpleDirectoryReader("./augustine_texts").load_data()

# Index them for retrieval
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

def get_context(query, author="Augustine"):
    """
    Retrieve relevant context for a given query.
    
    :param query: The query for which context is needed.
    :param author: The author whose texts are being queried.
    :return: Relevant passages as context.
    """
    # Query the index for relevant passages
    response = query_engine.query(query)
    
    # Return the response as context
    return response