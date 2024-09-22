import os
from dotenv import load_dotenv
from utils.system.logger import logger
from qdrant_client.http import models as rest

load_dotenv()
log = logger()

VECTOR_SIZE = os.getenv('VECTOR_SIZE')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')

def create_collection(qdrant):
    try:
        log.info('Creating Qdrant collection')
        qdrant.recreate_collection(
            collection_name = COLLECTION_NAME,
            vectors_config={
                'title': rest.VectorParams(
                    distance=rest.Distance.COSINE,
                    size = VECTOR_SIZE,
                    quantization_config=rest.ScalarQuantization(
                        scalar=rest.ScalarQuantizationConfig(
                            type=rest.ScalarType.INT8,
                            quantile=0.99,
                            always_ram=True,
                        ),
                    ),
                ),
                'content': rest.VectorParams(
                    distance=rest.Distance.COSINE,
                    size = VECTOR_SIZE,
                    quantization_config=rest.ScalarQuantization(
                        scalar=rest.ScalarQuantizationConfig(
                            type=rest.ScalarType.INT8,
                            quantile=0.99,
                            always_ram=True,
                        ),
                    ),
                ),
            }
        )
        log.info('Qdrant collection created')
    except Exception as e:
        log.error(f'An error has occurred while creating Qdrant collection "{COLLECTION_NAME}". {e}')