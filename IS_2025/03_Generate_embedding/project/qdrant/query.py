import os
import qdrant_client 
from dotenv import load_dotenv
from utils.logger import logger
from sentence_transformers import SentenceTransformer
from qdrant_client import models
from qdrant_client.http import models as rest

load_dotenv()
log = logger()

QDRANT_HOST = os.getenv('QDRANT_HOST')
QDRANT_PORT = os.getenv('QDRANT_PORT')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL')

def query_qdrant(query, vector_names=['text'], top_k=5, score_threshold=None, with_payload=True, hnsw_ef=256, exact=False, filters=None, qdrant=None, model=None,):
    if qdrant is None:
        qdrant = qdrant_client.QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    if model is None:
        model = SentenceTransformer(EMBEDDING_MODEL)
    embedded_query = model.encode(query).tolist()

    search_params = rest.SearchParams(
        hnsw_ef=hnsw_ef,
        exact=exact
    )

    # Construir filtro con should (OR)
    payload_filter = None
    if filters:
        should_conditions = []
        for key, value in filters.items():
            should_conditions.append(
                rest.FieldCondition(
                    key=key,
                    match=rest.MatchValue(value=value)
                )
            )
        payload_filter = rest.Filter(should=should_conditions)

    # Buscar con filtros (OR)
    filtered_results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=('text', embedded_query),
        limit=top_k,
        query_filter=payload_filter,
        search_params=search_params,
        with_payload=with_payload,
        score_threshold=score_threshold
    )

    # Si hay menos de top_k, completar con resultados sin filtro
    if len(filtered_results) < top_k:
        needed = top_k - len(filtered_results)

        unfiltered_results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=('text', embedded_query),
            limit=top_k + needed,
            query_filter=None,
            search_params=search_params,
            with_payload=with_payload,
            score_threshold=score_threshold
        )

        # Evitar duplicados
        filtered_ids = {res.id for res in filtered_results}
        non_duplicate_results = [res for res in unfiltered_results if res.id not in filtered_ids]

        filtered_results.extend(non_duplicate_results[:needed])

    # Ordenar por score y devolver top_k
    del embedded_query
    return sorted(filtered_results, key=lambda x: x.score, reverse=True)[:top_k]
