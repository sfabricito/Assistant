from sentence_transformers import SentenceTransformer
from .system.logger import logger

log = logger()

model = SentenceTransformer('all-mpnet-base-v2')

def generate_embeddings(text):
    try:
        log.info("Embedding generated succesfully")
        embedding = model.encode(text).tolist()
        return embedding
    except Exception as e:
        log.error(f'An error has occur while generating an embedding. {e}')