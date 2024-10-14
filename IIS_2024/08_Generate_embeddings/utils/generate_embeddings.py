from sentence_transformers import SentenceTransformer
from .system.logger import logger

log = logger()
model = SentenceTransformer('all-mpnet-base-v2')

def generate_embeddings(text):
    try:
        if isinstance(text, str) and text != '':
            embedding = model.encode(text).tolist()
            log.info("Embedding generated succesfully")
        else:
            embedding = model.encode('This embedding is not related with anything').tolist()
        return embedding
    except Exception as e:
        log.error(f'An error has occur while generating an embedding. {e}')