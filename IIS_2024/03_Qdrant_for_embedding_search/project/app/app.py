import qdrant_client 
from ..utils.console import console
from ..utils.read_data import read_data
from ..utils.load_data import load_data
from ..utils.create_collection import create_collection

if __name__=="__main__":
    article_df = read_data()

    qdrant = qdrant_client.QdrantClient(host="localhost", port=6333)

    create_collection(qdrant, len(article_df['content_vector'][0]))
    load_data(qdrant, article_df)

    console()