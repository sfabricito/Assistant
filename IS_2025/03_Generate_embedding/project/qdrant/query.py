import os
import qdrant_client 
from dotenv import load_dotenv
from utils.logger import logger
from sentence_transformers import SentenceTransformer
from qdrant_client import models

load_dotenv()
log = logger()

QDRANT_HOST = os.getenv('QDRANT_HOST')
QDRANT_PORT = os.getenv('QDRANT_PORT')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL')
log.error(f'Configuring Qdrant Client. Model: {EMBEDDING_MODEL}')

def query_qdrant(query, vector_names=['text'], top_k=20, score_threshold=None, with_payload=True, hnsw_ef=128, exact=False):
    qdrant = qdrant_client.QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    model = SentenceTransformer(EMBEDDING_MODEL)
    embedded_query = model.encode(query).tolist()

    search_params = models.SearchParams(
        hnsw_ef=hnsw_ef,  # Controls search accuracy/speed for HNSW
        exact=exact  # True for exact search, False for approximate search (faster)
    )

    combined_results = []

    query_results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=('text', embedded_query),
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
