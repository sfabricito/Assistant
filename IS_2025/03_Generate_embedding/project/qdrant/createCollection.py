import os
from dotenv import load_dotenv
from utils.logger import logger
from qdrant_client.http import models as rest

load_dotenv()
log = logger()

COLLECTION_NAME = os.getenv('COLLECTION_NAME')

def createCollection(qdrant, vector_size):
    try:
        log.info(f'Creating Qdrant collection. Collection name: "{COLLECTION_NAME}". Vector size: {vector_size}')
        qdrant.recreate_collection(
            collection_name = COLLECTION_NAME,
            vectors_config={
                'date': rest.VectorParams(
                    distance=rest.Distance.COSINE,
                    size = vector_size,
                    quantization_config=rest.ScalarQuantization(
                        scalar=rest.ScalarQuantizationConfig(
                            type=rest.ScalarType.INT8,
                            quantile=0.99,
                            always_ram=True,
                        ),
                    ),
                ),
                'location': rest.VectorParams(
                    distance=rest.Distance.COSINE,
                    size = vector_size,
                    quantization_config=rest.ScalarQuantization(
                        scalar=rest.ScalarQuantizationConfig(
                            type=rest.ScalarType.INT8,
                            quantile=0.99,
                            always_ram=True,
                        ),
                    ),
                ),
                'attack_type': rest.VectorParams(
                    distance=rest.Distance.COSINE,
                    size = vector_size,
                    quantization_config=rest.ScalarQuantization(
                        scalar=rest.ScalarQuantizationConfig(
                            type=rest.ScalarType.INT8,
                            quantile=0.99,
                            always_ram=True,
                        ),
                    ),
                ),
                'target_type': rest.VectorParams(
                    distance=rest.Distance.COSINE,
                    size = vector_size,
                    quantization_config=rest.ScalarQuantization(
                        scalar=rest.ScalarQuantizationConfig(
                            type=rest.ScalarType.INT8,
                            quantile=0.99,
                            always_ram=True,
                        ),
                    ),
                ),
                'corporation': rest.VectorParams(
                    distance=rest.Distance.COSINE,
                    size = vector_size,
                    quantization_config=rest.ScalarQuantization(
                        scalar=rest.ScalarQuantizationConfig(
                            type=rest.ScalarType.INT8,
                            quantile=0.99,
                            always_ram=True,
                        ),
                    ),
                ),
                'target': rest.VectorParams(
                    distance=rest.Distance.COSINE,
                    size = vector_size,
                    quantization_config=rest.ScalarQuantization(
                        scalar=rest.ScalarQuantizationConfig(
                            type=rest.ScalarType.INT8,
                            quantile=0.99,
                            always_ram=True,
                        ),
                    ),
                ),
                'orchestrating_group': rest.VectorParams(
                    distance=rest.Distance.COSINE,
                    size = vector_size,
                    quantization_config=rest.ScalarQuantization(
                        scalar=rest.ScalarQuantizationConfig(
                            type=rest.ScalarType.INT8,
                            quantile=0.99,
                            always_ram=True,
                        ),
                    ),
                ),
                'weapon': rest.VectorParams(
                    distance=rest.Distance.COSINE,
                    size = vector_size,
                    quantization_config=rest.ScalarQuantization(
                        scalar=rest.ScalarQuantizationConfig(
                            type=rest.ScalarType.INT8,
                            quantile=0.99,
                            always_ram=True,
                        ),
                    ),
                ),
                'notes': rest.VectorParams(
                    distance=rest.Distance.COSINE,
                    size = vector_size,
                    quantization_config=rest.ScalarQuantization(
                        scalar=rest.ScalarQuantizationConfig(
                            type=rest.ScalarType.INT8,
                            quantile=0.99,
                            always_ram=True,
                        ),
                    ),
                ),
                'scite1': rest.VectorParams(
                    distance=rest.Distance.COSINE,
                    size = vector_size,
                    quantization_config=rest.ScalarQuantization(
                        scalar=rest.ScalarQuantizationConfig(
                            type=rest.ScalarType.INT8,
                            quantile=0.99,
                            always_ram=True,
                        ),
                    ),
                ),
                'scite2': rest.VectorParams(
                    distance=rest.Distance.COSINE,
                    size = vector_size,
                    quantization_config=rest.ScalarQuantization(
                        scalar=rest.ScalarQuantizationConfig(
                            type=rest.ScalarType.INT8,
                            quantile=0.99,
                            always_ram=True,
                        ),
                    ),
                ),
                'scite3': rest.VectorParams(
                    distance=rest.Distance.COSINE,
                    size = vector_size,
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