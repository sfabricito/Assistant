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
                'date': rest.VectorParams(
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
                'location': rest.VectorParams(
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
                'attack_type': rest.VectorParams(
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
                'target_type': rest.VectorParams(
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
                'corporation': rest.VectorParams(
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
                'target': rest.VectorParams(
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
                'orchestrating_group': rest.VectorParams(
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
                'weapon': rest.VectorParams(
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
                'notes': rest.VectorParams(
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
                'scite1': rest.VectorParams(
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
                'scite2': rest.VectorParams(
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
                'scite3': rest.VectorParams(
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