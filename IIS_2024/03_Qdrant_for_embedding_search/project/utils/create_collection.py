from qdrant_client.http import models as rest

def create_collection(qdrant, vector_size):
    qdrant.recreate_collection(
        collection_name='Articles',
        vectors_config={
            'title': rest.VectorParams(
                distance=rest.Distance.COSINE,
                size=vector_size,
            ),
            'content': rest.VectorParams(
                distance=rest.Distance.COSINE,
                size=vector_size,
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