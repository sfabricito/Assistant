import openai

EMBEDDING_MODEL = "text-embedding-ada-002"

def query_qdrant(qdrant, query, collection_name, vector_name='title', top_k=20):
    print("-----------------------------------------")
    print("Query request")
    embedded_query = openai.embeddings.create(
        input=query,
        model=EMBEDDING_MODEL,
    ).data[0].embedding
    
    query_results = qdrant.search(
        collection_name=collection_name,
        query_vector=(vector_name, embedded_query),
        limit=top_k, 
        query_filter=None
    )
    
    return query_results