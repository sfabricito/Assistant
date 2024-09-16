import qdrant_client 
from utils.read_data import read_data
from utils.load_data import load_data
from utils.download_data import download_data
from utils.create_collection import create_collection
from utils.reduce_csv import reduce_csv

if __name__=="__main__":
    print('Downloading')
    download_data('https://cdn.openai.com/API/examples/data/vector_database_wikipedia_articles_embedded.zip')
    print('Reading')
    reduce_csv("./data/vector_database_wikipedia_articles_embedded.csv", "./data/small_vector_database_wikipedia_articles_embedded.csv", 1500)
    article_df = read_data()
    print('Setting up Qdrant')
    qdrant = qdrant_client.QdrantClient(host="localhost", port=6333)
    print('Creating Qdrant collection')
    create_collection(qdrant, len(article_df['content_vector'][0]))
    print('loading data')
    load_data(qdrant, article_df)