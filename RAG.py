from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex

# Load Augustine’s texts
documents = SimpleDirectoryReader("./augustine_texts").load_data()

# Index them for retrieval
index = GPTVectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# Ask a question dynamically
response = query_engine.query("What does Augustine say about grace?")
print(response)