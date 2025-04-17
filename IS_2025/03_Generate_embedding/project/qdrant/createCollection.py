import os
from dotenv import load_dotenv
from utils.logger import logger
from qdrant_client.http import models as rest

load_dotenv()
log = logger()

COLLECTION_NAME = os.getenv('COLLECTION_NAME')

distances = {
    'Cosine Similiarity': rest.Distance.COSINE,
    'Euclidean Distance': rest.Distance.EUCLID,
    'Dot Product': rest.Distance.DOT,
}

def createCollection(qdrant, distance, vector_size):
    try:
        log.info(f'Creating Qdrant collection. Collection name: "{COLLECTION_NAME}". Vector size: {vector_size}')
        qdrant.recreate_collection(
            collection_name = COLLECTION_NAME,
            vectors_config={
                'text': rest.VectorParams(
                    distance=distances[distance],
                    size = vector_size,
                    quantization_config=rest.ScalarQuantization(
                        scalar=rest.ScalarQuantizationConfig(
                            type=rest.ScalarType.INT8,
                            quantile=0.99,
                            always_ram=True,
                        ),
                    ),
                )
            }
        )
        log.info('Qdrant collection created')
    except Exception as e:
        log.error(f'An error has occurred while creating Qdrant collection "{COLLECTION_NAME}". {e}')