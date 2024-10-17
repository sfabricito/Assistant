import os
from dotenv import load_dotenv
from .system.logger import logger
from .generate_embeddings import generate_embeddings
from qdrant_client import models

load_dotenv()
log = logger()

COLLECTION_NAME = os.getenv('COLLECTION_NAME')

def query_qdrant(qdrant, query, vector_names=['location'], top_k=20, score_threshold=None, with_payload=True, hnsw_ef=128, exact=False):
    # Generate the embedded query vector
    embedded_query = generate_embeddings(query)

    # Construct the search parameters
    search_params = models.SearchParams(
        hnsw_ef=hnsw_ef,  # Controls search accuracy/speed for HNSW
        exact=exact  # True for exact search, False for approximate search (faster)
    )

    combined_results = []

    # Perform searches for each vector name
    for vector_name in vector_names:
        log.info(f"Searching using vector_name: {vector_name}")
        
        query_results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=(vector_name, embedded_query),
            limit=top_k, 
            query_filter=None,  # Add filters here if needed
            search_params=search_params,
            with_payload=with_payload,  # Include payload in the result
            score_threshold=score_threshold  # Optional filtering by score
        )
        
        # Combine the results from each vector search
        combined_results.extend(query_results)

    # Sort combined results by score (descending) and limit to top_k
    combined_results = sorted(combined_results, key=lambda x: x.score, reverse=True)[:top_k]

    return combined_results

def print_query_results(query_results):
    if not query_results:
        print("No results found.")
        return
    
    print(f"Found {len(query_results)} results:")
    
    for i, result in enumerate(query_results):
        print(f"\nResult {i+1}:")
        print(f"  Score: {result.score}")
        
        if result.payload:
            print("  Payload:")
            for key, value in result.payload.items():
                print(f"    {key}: {value}")
        else:
            print("  No payload available.")

    print("\nEnd of results.")
